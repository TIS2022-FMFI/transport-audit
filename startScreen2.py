from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from skener import Scanner
from sqlite import User
from random import randint
class StartScreen(Screen):
    def __init__(self, povodna, dalsia, aplikacia, **kwargs):
        super().__init__(**kwargs)
        self.povodna = povodna
        self.dalsia = dalsia
        self.kodZamestnanca = []
        self.aplikacia = aplikacia
        self.skenovanieScreen = Scanner(self.aplikacia.screenManager, self.kodZamestnanca, self.name, self.name, name='skener')
        self.aplikacia.screenManager.add_widget(self.skenovanieScreen)
        self.skenovanieScreen.prveSpustenie = False

        bSkenovanie = Button(text='Naskenujte svoj kod', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 0.5, "top":0.5}, size_hint =(0.3, 0.08))
        bSkenovanie.bind(on_press=self.skenovanie)
        self.add_widget(bSkenovanie)

        logo = Image(source='logo.webp')
        logo.size_hint_x = 0.2
        logo.pos_hint = {'center_x': 0.5, 'top': 1.3}
        self.add_widget(logo)

        bJazyk = Button(text='Vyber jazyka', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.5, "top": 0.15}, size_hint=(0.3, 0.08))
        # bPokracovat.bind(on_press=self.skeno)
        self.add_widget(bJazyk)
        self.bind(on_enter=self.kontrolaPrihlasenia)




    def skenovanie(self, *args):
        self.aplikacia.screenManager.current = self.skenovanieScreen.name

    def kontrolaPrihlasenia(self, *args):
        #self.scrollZakaznici.vynuluj()
        #self.scrollAuta.vynuluj()
        print(self.kodZamestnanca, self.aplikacia.zamestnanec)
        if not self.kodZamestnanca:
            return


        pouzivatel = User().stiahni(self.kodZamestnanca[0])
        if pouzivatel is None:
            pouz = User().vrat_vsetky(True)
            ind = randint(0, len(pouz)-1 )
            pouzivatel = pouz[ind]
        if pouzivatel is not None and not pouzivatel.over_zmazanie():

            self.aplikacia.zamestnanec = pouzivatel
            print("bol najdeny zamestnanec", self.aplikacia.zamestnanec, pouzivatel)
            self.kodZamestnanca.clear()
            self.aplikacia.screenManager.current = self.dalsia
        else:
            self.kodZamestnanca.clear()
            popup = Popup(title='Prihlasenie neprebehlo', content=Label(text='Nepodarilo sa najst zamestnanca s naskenovanym kodom'),size_hint=(0.5, 0.5))
            popup.open()
            #self.aplikacia.screenManager.current = self.dalsia
            #self.aplikacia.screenManager.current = self.aplikacia.auditUvodScreen.name
