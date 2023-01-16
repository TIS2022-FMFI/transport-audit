from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Vehicle
class Edit_Vehicles (BoxLayout):
    select_id  = None
    notify = Button(text = '')
    text1 = TextInput(text='ŠPZ')
    drop1 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    vehicle_list = None
    screenManager = None
    values=[]
    def __init__(self,screenManager, **kwargs):
        super(Edit_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
        self.text1 = self.ids.input_edit_vehicle
    def synchronize_vehicles(self):
        self.select_id = None
        self.values = []
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.vehicle_list:
            self.values.append(i)
        self.ids.spinner_edit_vehicle.values = self.values
        self.ids.spinner_edit_vehicle.text = 'Vyber ŠPZ na úpravu'
    def set_widgets(self,tex1):
        if tex1 not in self.vehicle_list:
            self.text1.text = ""
            return
        self.text1.text = tex1
        self.select_id = self.vehicle_list[tex1]
    def call_Back (self):
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        print(self.text1)
        if (self.select_id is None):
            self.notify.text = "Nie je vybratá ŠPZ."
        elif len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')) or (ord(x) == ' ') or (ord(x) >= ord('0') and ord(x) <= ord('9')))]) != len(self.text1.text) or self.text1.text == "ŠPZ":
            self.notify.text = "ŠPZ je v zlom formáte."
        elif self.text1.text == "":
            self.notify.text = "ŠPZ je v zlom formáte."
        elif self.text1.text in self.vehicle_list.keys() and self.vehicle_list[self.text1.text]!= self.select_id:
            self.notify.text = "ŠPZ už existuje."
        else:
            updated_vehicle = Vehicle().stiahni(self.select_id)
            updated_vehicle.SPZ = self.text1.text
            updated_vehicle.update()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.text1.text = ''
        self.synchronize_vehicles()