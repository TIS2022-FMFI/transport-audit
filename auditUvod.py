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

from sqlite import Customer, Vehicle







"""
class Customer:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Vehicle:
    def __init__(self, name):
        self.SPZ = name

    def get_name(self):
        return self.SPZ

customers = [Customer("aaa"), Customer("bbbbb"), Customer("ccc"), Customer("DDD")]
SPZ = [Vehicle("SC"), Vehicle("BA"), Vehicle("NM"), Vehicle("KE"), Vehicle("BB")]
"""

from priebehAuditu import PrebiehajuciAudit
class UvodAuditu(Screen):
    class ScrollbarVyber:
        def __init__(self, prvky, text, screen, y):

            pouz = set()
            self.naVyber = []
            for p in prvky:
                if p.Name is not None:# and p.Name not in pouz:
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

            self.uvodnaPonuka(None, None)

        def scroll_change(self, scrlv, instance, value):
            scrlv.scroll_y = value

        def slider_change(self, s, instance, value):
            if value >= 0:
                s.value = value

        def vyberPoloziek(self):
            if isinstance(self.naVyber[0], Vehicle) and self.druhyScrollbar.vybrate is None:
                return
            print(self.buttonHlavny, "Rreefsjkshcjksdhcksh", self.root)
            self.screen.remove_widget(self.buttonHlavny)
            self.buttonHlavny.parent = None

            if self.root is None:
                self.layout2 = GridLayout(cols=1, spacing=10, size_hint_y=None)
                self.layout2.bind(minimum_height=self.screen.setter('height'))
                for polozka in self.naVyber:
                    btn = Button(text=polozka.Name, size_hint_y=None, height=40, background_color="#0003a8",
                                 background_normal="")
                    btn.bind(on_press=partial(self.uvodnaPonuka, polozka))
                    self.buttonyVyber.append(btn)
                self.root = ScrollView(size_hint=(0.8, 0.3), pos_hint={'center_y': self.y, 'center_x': 0.5},
                                       do_scroll_x=False,
                                       do_scroll_y=True, bar_color=(1, 0, 0, 1), bar_width=50)
                self.slider = Slider(min=0, max=9, value=5, orientation="vertical", step=0.01, size_hint=(0.1, 0.3),
                                     pos_hint={'center_y': self.y, 'center_x': 0.95})
                self.root.bind(scroll_y=partial(self.slider_change, self.slider))
                self.slider.bind(value=partial(self.scroll_change, self.root))
                self.root.add_widget(self.layout2)

            for btn in self.buttonyVyber:
                self.layout2.add_widget(btn)
            self.screen.add_widget(self.slider)
            self.screen.add_widget(self.root)

        def uvodnaPonuka(self, vybrate, button):
            text = self.text
            if vybrate is not None:
                self.vybrate = vybrate
                text = vybrate.Name

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
            if self.vybrate is None:
                return
            self.screen.remove_widget(self.buttonHlavny)
            self.vybrate = None
            self.uvodnaPonuka(None, True)





    def __init__(self, aplikacia, povodna, dalsia, **kwargs):
        super().__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.dalsia = dalsia

        bPokracovat = Button(text='Pokracovat', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 0.5, "top":0.2}, size_hint =(1, 0.08))
        bPokracovat.bind(on_press=self.pokracovat)
        self.add_widget(bPokracovat) #upravit, toto je len na skusku
        bOdhlasenie = Button(text='Odhlasit', pos_hint={"top":0.1, 'center_x': 0.5}, background_color="#0003a8",
                                    background_normal="",size_hint =(1, 0.08))
        bOdhlasenie.bind(on_press=self.odhlasit)
        self.add_widget(bOdhlasenie)

        self.scrollZakaznici = UvodAuditu.ScrollbarVyber(Customer().vrat_vsetky(True), 'Zakaznici', self, 0.75)
        self.scrollAuta =  UvodAuditu.ScrollbarVyber(Vehicle().vrat_vsetky(True), 'SPZ', self, 0.40)
        self.scrollAuta.druhyScrollbar = self.scrollZakaznici
        self.prvyVstup = True
        self.bind(on_enter = self.povodnyStav)


    def povodnyStav(self, *args):
        if self.prvyVstup:
            self.prvyVstup = False
            return

        self.scrollZakaznici.vynuluj()
        self.scrollAuta.vynuluj()

    def odhlasit(self, *args):
        #self.aplikacia.screenManager.current = self.povodna
        print("odhladujem")
        self.aplikacia.zamestnanec = None
        self.povodna.kodZamestnanca.clear()
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
        self.dalsia = PrebiehajuciAudit(self.aplikacia, self, self.scrollZakaznici.vybrate, self.scrollAuta.vybrate, name='priebeh'+str(self.aplikacia.auditov))
        self.aplikacia.screenManager.add_widget(self.dalsia)
        self.aplikacia.screenManager.current = self.dalsia.name