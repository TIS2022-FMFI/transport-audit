from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Vehicle
class Add_Vehicles (BoxLayout):    
    notify = Button(text = '')
    text1 = TextInput(text='SPZ')
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Späť")
    screenManager = None
    vehicle_list = None
    def synchronize_vehicles(self):
        self.vehicle_list = [i['SPZ'] for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def __init__(self, screenManager,**kwargs):
        super(Add_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(self.text1)        
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)    
    def call_Back (self):
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        if  len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')) or (ord(x) == ' ') or (ord(x)>=ord('0') and ord(x)<= ord('9')))]) != len(self.text1.text) or self.text1.text == "SPZ":
            self.notify.text = "Please enter a valid SPZ"
        elif self.text1.text in self.vehicle_list:
            self.notify.text = "SPZ already exists"
        elif self.text1.text in [i['SPZ'] for i in Vehicle().vrat_vsetky()]:
            self.notify.text = "SPZ already exists"
        else:
            Vehicle().nahraj(self.text1.text)
            self.call_Back()

    def clear_screen(self, *args):
        self.notify.text = ""
        self.text1.text = 'SPZ'
        self.synchronize_vehicles()