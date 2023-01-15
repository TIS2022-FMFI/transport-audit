import time
import sqlite3

from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from dateutil.parser import parse

from datetime import datetime

from kivy.uix.textinput import TextInput

from skener import Scanner

from sqlite import User, User_Role


class UzavretyKamion(Screen):
    def __init__(self, aplikacia, povodna, dalsia, **kwargs):
        super().__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.dalsia = dalsia
        self.potvrdenie = False
        self.kod = []





        self.bind(on_enter=self.kontrolaPatternu)
    def skenovanie(self, *args):
        self.aplikacia.screenManager.current  = self.aplikacia.skenovanieScreen.name
    def kontrolaPatternu(self, *args):
        self.screen()
        if not self.aplikacia.kod:
            splneniePatternu = self.povodna.kontrolaSplneniaPatternu()
            print(("pattern ", splneniePatternu))
            if splneniePatternu != 0:
                #self.bsken.parent = None
                self.add_widget(self.bsken)
                self.potvrdenie = False
            else:

                self.remove_widget(self.bsken)
                self.potvrdenie = True
            return
        zamestnanec = User().stiahni(self.aplikacia.kod[0])
        if zamestnanec is not None and not zamestnanec.over_zmazanie():
            self.potvrdenie = False

            rola = User_Role().stiahni(zamestnanec.User_Role_id)
            if rola is not None and not rola.over_zmazanie() and (rola.name == 'Operátor' or rola.name == 'Administrátor'):
                self.potvrdenie = True
                self.aplikacia.kod.clear()
                self.remove_widget(self.bsken)
                return
        popup = Popup(title='Autentifikacia neprebehla',
                      content=Label(text='Nebol najdeny zamestanec s naskenovanym kodom alebo nemal potrebne opravnenie'),
                      size_hint=(0.5, 0.5))
        popup.open()
        self.aplikacia.kod.clear()
        self.potvrdenie = False
        self.add_widget(self.bsken)


    def otvorit(self, *args):
        self.aplikacia.kod.clear()
        self.aplikacia.screenManager.current = self.povodna.name

    def screen(self):
        self.aplikacia.skenovanieScreen.povodnaScreen = self.name
        self.aplikacia.skenovanieScreen.dalsiaScreen = self.name
        # self.clear_widgets()
        # logo = Image(source='logo.webp')
        # logo.size_hint_x = 0.2
        # logo.pos_hint = {'center_x': 0.5, 'top': 1.3}
        # self.add_widget(logo)

        self.lUzavrete = Label(text='Vozidlo je uzavrete', pos_hint={'center_x': 0.5, "top": 0.5},
                               size_hint=(1, 0.12), font_size='30sp', color=[0, 0, 0])
        # self.lUzavrete = Text(text='Vozidlo je uzavrete', pos_hint={'center_x': 0.5, "top": 0.5},
        #                        size_hint=(1, 0.12), font_size='30sp', background_color=[1, 1, 1])
        self.add_widget(self.lUzavrete)

        from kivy.utils import rgba
        bOtvorit = Button(text='Otvorit vozidlo', background_color=rgba('#021D49'),
                          background_normal="", pos_hint={'center_x': 0.5, "top": 0.2}, size_hint=(1, 0.08))
        bOtvorit.bind(on_press=self.otvorit)
        self.add_widget(bOtvorit)

        bNovyAudit = Button(text='Dalsi audit', background_color=rgba('#021D49'),
                            background_normal="", pos_hint={'center_x': 0.5, "top": 0.1}, size_hint=(1, 0.08))
        bNovyAudit.bind(on_press=self.novyAudit)
        self.add_widget(bNovyAudit)
        self.bsken = Button(text='Potvrdit porusenie patternu', background_color=rgba('#021D49'),
                            background_normal="", pos_hint={'center_x': 0.5, "top": 0.3}, size_hint=(1, 0.08))
        self.bsken.bind(on_press=self.skenovanie)
    def novyAudit(self, *args):

        if not self.potvrdenie:
            popup = Popup(title='Porusenie patternu',
                          content=Label(text='Pre uzavretie auditu musite potrvdit porusenie patternu'), size_hint=(0.5, 0.5))
            popup.open()
            return


        s = self.aplikacia.shippment
        shippment = self.aplikacia.shippment.nahraj(s.User_code, str(parse(str(datetime.now()))), s.Customer_id, s.Vehicle_id)
        if shippment is not None:
            for v in self.aplikacia.shippmentStillages:
                v.Shipment_id = shippment.id
                v.nahraj(v.Date_time_start, v.Date_time_end, v.Stillage_number, v.Stillage_Number_on_Header,
                         v.First_scan_product, v.Last_scan_product, v.JLR_Header_NO, v.Carriage_L_JLR_H,
                         v._Check, v.First_scan_TLS_code, v.Last_scan_TLS_code, v.Stillage_Type_id, v.Shipment_id, v.TLS_range_start, v.TLS_range_stop, v.Note)
        self.povodna.spat()