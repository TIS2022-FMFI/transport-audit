from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Vehicle
class Add_Vehicles (BoxLayout):
    """
    pridavanie SPZ vozidiel
    """
    notify = Button(text = '')
    text1 = TextInput(text='ŠPZ')
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Späť")
    screenManager = None
    vehicle_list = None
    def synchronize_vehicles(self):
        """
        natiahne SPZ z databazy
        """
        self.vehicle_list = [i['SPZ'] for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def __init__(self, screenManager,**kwargs):
        super(Add_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_vehicle
        self.notify = self.ids.notify
    def call_Back (self):
        """
        vrati sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne prida SPZ do databazy
        """
        if  len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')) or (ord(x) == ' ') or (ord(x)>=ord('0') and ord(x)<= ord('9')))]) != len(self.text1.text) or self.text1.text == "ŠPZ":
            self.notify.text = "ŠPZ je v zlom formáte."
        elif self.text1.text == "":
            self.notify.text = "Nie je zadaná ŠPZ."
        elif self.text1.text in self.vehicle_list:
            self.notify.text = "ŠPZ už existuje."
        elif self.text1.text in [i['SPZ'] for i in Vehicle().vrat_vsetky()]:
            self.notify.text = "ŠPZ už existuje."
        else:
            Vehicle().nahraj(self.text1.text)
            self.call_Back()

    def clear_screen(self, *args):
        """
        nacitanie udajov
        """
        self.notify.text = ""
        self.text1.text = ''
        self.synchronize_vehicles()