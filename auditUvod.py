from functools import partial

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
#from scanner import *
from kivy.uix.dropdown import  DropDown
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget

from sqlite import Customer, Vehicle, Pattern, Config



class ScrollbarVyber:
    def __init__(self, prvky, text, screen, y):

        pouz = set()
        self.naVyber = []
        for p in prvky:
            if p.Name is not None:  # and p.Name not in pouz:
                pouz.add(p.Name)
                self.naVyber.append(p)
        self.vybrate = None
        self.screen = screen
        self.buttonHlavny = None
        self.buttonyVyber = []
        self.layout2 = None
        self.slider = None
        self.text = text
        self.root = None
        self.y = y
        self.druhyScrollbar = None
        self.polozkyZobrazene = False

        self.uvodnaPonuka(None, None)

    def scroll_change(self, scrlv, instance, value):
        scrlv.scroll_y = value

    def slider_change(self, s, instance, value):
        if value >= 0:
            s.value = value

    def vyberPoloziek(self):
        if not self.naVyber:
            return
        if isinstance(self.naVyber[0], Vehicle) and self.druhyScrollbar.vybrate is None:
            return
        self.polozkyZobrazene = True
        self.vybrate= None

        self.screen.remove_widget(self.buttonHlavny)
        self.buttonHlavny.parent = None

        if self.root is None:
            self.layout2 = GridLayout(cols=1, spacing=10, size_hint_y=None)
            self.layout2.bind(minimum_height=self.screen.setter('height'))

            self.root = ScrollView(size_hint=(0.8, 0.3), pos_hint={'center_y': self.y, 'center_x': 0.5},
                                   do_scroll_x=False,
                                   do_scroll_y=True, bar_color=(1, 0, 0, 1), bar_width=50)
            self.slider = Slider(min=0, max=9, value=5, orientation="vertical", step=0.01, size_hint=(0.1, 0.3),
                                 pos_hint={'center_y': self.y, 'center_x': 0.95})
            self.root.bind(scroll_y=partial(self.slider_change, self.slider))
            self.slider.bind(value=partial(self.scroll_change, self.root))
            self.root.add_widget(self.layout2)

        self.buttonyVyber = []
        for polozka in self.naVyber:
            btn = Button(text=polozka.Name, size_hint_y=None, height=40, background_color="#0003a8",
                         background_normal="")
            btn.bind(on_press=partial(self.uvodnaPonuka, polozka))
            self.buttonyVyber.append(btn)
            self.layout2.add_widget(btn)


        self.screen.add_widget(self.slider)
        self.screen.add_widget(self.root)

    def uvodnaPonuka(self, vybrate, button):
        self.polozkyZobrazene = False
        text = self.text
        if vybrate is not None:
            self.vybrate = vybrate
            text = vybrate.Name
            if self.naVyber and isinstance(self.naVyber[0], Customer):
                idAutZakaznika = set([x.Vehicle_id for x in Config().configyZakaznika(self.vybrate.id)])
                #print(idAutZakaznika, "configy", self.vybrate.id)
                if self.druhyScrollbar.vybrate is None:
                    self.druhyScrollbar.vynuluj()
                #print([[x.SPZ, x.id] for x in self.druhyScrollbar.naVyber])
                self.druhyScrollbar.naVyber.sort(key = lambda x : x.id in idAutZakaznika, reverse=True)
                #print([[x.SPZ, x.id] for x in self.druhyScrollbar.naVyber])


        self.buttonHlavny = Button(text=text, pos_hint={"center_y": self.y}, background_color="#dddddd",
                                   background_normal="", color="#1c1b1d", size_hint=(1, 0.08))
        self.buttonHlavny.bind(on_press=lambda x: self.vyberPoloziek())
        self.screen.add_widget(self.buttonHlavny)
        if button is None:
            return

        for b in self.buttonyVyber:
            self.layout2.remove_widget(b)
        self.screen.remove_widget(self.layout2)
        self.screen.remove_widget(self.slider)
        self.root.parent = None

    def vynuluj(self):
        if self.polozkyZobrazene:
            #print(self.naVyber[0].Name)
            self.uvodnaPonuka(None, False)
            return
        if self.vybrate is None:
            return
        self.screen.remove_widget(self.buttonHlavny)
        self.vybrate = None
        self.uvodnaPonuka(None, True)



from priebehAuditu import PrebiehajuciAudit
class UvodAuditu(Screen):

    def __init__(self, aplikacia, povodna, dalsia, **kwargs):
        super().__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.dalsia = dalsia

        bPokracovat = Button(text='Pokracovat', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 0.5, "top":0.2}, size_hint =(1, 0.08))
        bPokracovat.bind(on_press=self.pokracovat)
        self.add_widget(bPokracovat)
        bOdhlasenie = Button(text='Odhlasit', pos_hint={"top":0.1, 'center_x': 0.5}, background_color="#0003a8",
                                    background_normal="",size_hint =(1, 0.08))
        bOdhlasenie.bind(on_press=self.odhlasit)
        self.add_widget(bOdhlasenie)

        self.scrollZakaznici = ScrollbarVyber([x for x in Customer().vrat_vsetky(True) if not x.over_zmazanie() and Pattern().patternZakaznika(x.id) is not None], 'Zakaznici', self, 0.75)
        self.scrollAuta =  ScrollbarVyber([x for x in Vehicle().vrat_vsetky(True) if not x.over_zmazanie()], 'SPZ', self, 0.40)
        self.scrollAuta.druhyScrollbar = self.scrollZakaznici
        self.scrollZakaznici.druhyScrollbar = self.scrollAuta
        self.prvyVstup = True
        self.bind(on_enter = self.povodnyStav)


    def povodnyStav(self, *args):
        self.scrollZakaznici.naVyber = [x for x in Customer().vrat_vsetky(True) if
                                        not x.over_zmazanie() and Pattern().patternZakaznika(x.id) is not None]
        self.scrollAuta.naVyber = [x for x in Vehicle().vrat_vsetky(True) if not x.over_zmazanie()]
        if self.prvyVstup:
            self.prvyVstup = False
            return
        self.scrollZakaznici.vynuluj()
        self.scrollAuta.vynuluj()

    def odhlasit(self, *args):
        #self.aplikacia.screenManager.current = self.povodna
        print("odhladujem")
        self.aplikacia.zamestnanec = None
        self.aplikacia.kod.clear()
        self.aplikacia.screenManager.current = self.povodna.name

    def pokracovat(self, *args):
        #self.scrollZakaznici.vynuluj()
        #self.scrollAuta.vynuluj()
        if self.scrollZakaznici.vybrate is None:
            popup = Popup(title='Nie je mozne pokracovat v audite',
                          content=Label(text='Nie je vybraty zakaznik'),
                          size_hint=(0.5, 0.5))
            popup.open()
            return
        elif self.scrollAuta.vybrate is None:
            popup = Popup(title='Nie je mozne pokracovat v audite',
                          content=Label(text='Nie je vybrane vozidlo'),
                          size_hint=(0.5, 0.5))
            popup.open()
            return

        self.aplikacia.auditov += 1

        self.aplikacia.prebiehajuciAudit.zakaznik = self.scrollZakaznici.vybrate
        self.aplikacia.prebiehajuciAudit.auto = self.scrollAuta.vybrate
        self.aplikacia.screenManager.current = self.aplikacia.prebiehajuciAudit.name