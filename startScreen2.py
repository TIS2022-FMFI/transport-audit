from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.utils import rgba

from sqlite import User, User_Role

class StartScreen(Screen):
    def __init__(self, povodna, dalsia, aplikacia, **kwargs):
        super().__init__(**kwargs)
        self.povodna = povodna
        self.dalsia = dalsia
        self.kodZamestnanca = []
        self.aplikacia = aplikacia


        # bSkenovanie = Button(text='Naskenujte svoj kod', background_color="#0003a8",
        #                             background_normal="", pos_hint = {'center_x': 0.5, "top":0.5}, size_hint =(0.3, 0.08))
        # bSkenovanie.bind(on_press=self.skenovanie)
        # self.add_widget(bSkenovanie)
        bSkenovanie = self.ids.btnSC
        bSkenovanie.bind(on_press=self.skenovanie)

        # logo = Image(source='logo.webp')
        # logo.size_hint_x = 0.2
        # logo.pos_hint = {'center_x': 0.5, 'top': 1.3}
        # self.add_widget(logo)

        # bJazyk = Button(text='Vyber jazyka', background_color="#0003a8",
        #                      background_normal="", pos_hint={'center_x': 0.5, "top": 0.15}, size_hint=(0.3, 0.08))
        # bPokracovat.bind(on_press=self.skeno)
        # self.add_widget(bJazyk)
        # self.bind(on_enter=self.kontrolaPrihlasenia)
        bJazyk = self.ids.btnJ

        self.bind(on_enter=self.kontrolaPrihlasenia)


    def skenovanie(self, *args):
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def kontrolaPrihlasenia(self, *args):
        self.aplikacia.skenovanieScreen.povodnaScreen = self.name
        self.aplikacia.skenovanieScreen.dalsiaScreen = self.name

        print(self.aplikacia.kod, self.aplikacia.zamestnanec)
        if not self.aplikacia.kod:
            return


        pouzivatel = User().stiahni(self.aplikacia.kod[0])
        if pouzivatel is not None and not pouzivatel.over_zmazanie() and User_Role().stiahni(pouzivatel.User_Role_id) is not None:

            self.aplikacia.zamestnanec = pouzivatel
            print("bol najdeny zamestnanec", self.aplikacia.zamestnanec, pouzivatel)
            self.aplikacia.kod.clear()
            self.aplikacia.screenManager.current = self.dalsia
        else:
            self.aplikacia.kod.clear()
            popup = Popup(title='Prihlásenie neprebehlo', content=Label(text='Nepodarilo sa nájsť zamestnanca s naskenovaným kódom'),size_hint=(0.5, 0.5))
            popup.open()

