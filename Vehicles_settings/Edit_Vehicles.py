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
    text1 = TextInput(text='SPZ')
    drop1 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    vehicle_list = None
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Edit_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton1 = Button(text='Vyber SPZ na upravu', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))        
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(self.text1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)

    def synchronize_vehicles(self):
        self.select_id = None
        self.drop1.clear_widgets()
        self.drop1.select('Vyber SPZ na upravu')
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.vehicle_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_widgets(btn.text))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def set_widgets(self,tex1):
        self.text1.text = tex1
        self.select_id = self.vehicle_list[tex1]
    def call_Back (self):
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        if (self.select_id is None):
            self.notify.text = "Please choose SPZ by id you want edit."
        elif len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')) or (ord(x) == ' ') or (ord(x) >= ord('0') and ord(x) <= ord('9')))]) != len(self.text1.text) or self.text1.text == "SPZ":
            self.notify.text = "Please enter a valid SPZ"
        elif self.text1.text in self.vehicle_list.keys() and self.vehicle_list[self.text1.text]!= self.select_id:
            self.notify.text = "This SPZ already exists"
        else:
            updated_vehicle = Vehicle().stiahni(self.select_id)
            updated_vehicle.SPZ = self.text1.text
            updated_vehicle.update()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.text1.text = 'SPZ'
        self.synchronize_vehicles()