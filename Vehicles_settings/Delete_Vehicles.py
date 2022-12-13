from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Vehicle
class Delete_Vehicles (BoxLayout):
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    vehicle_list = None
    screenManager = None
    def synchronize_vehicles(self):
        self.on_delete_selected = None
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.drop1.clear_widgets()
        self.drop1.select('Vyber vozidlo na vymazanie')
        for i in self.vehicle_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.select_id(btn.text))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def __init__(self,screenManager, **kwargs):
        super(Delete_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton1 = Button(text='Vyber vozidlo na vymazanie', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())        
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def select_id(self,tex):
        self.on_delete_selected  = self.vehicle_list[tex]
    def call_Back (self):
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Please choose Vehicle by id you want delete."
        else:
            on_delete_Vehicle = Vehicle().stiahni(self.on_delete_selected)
            on_delete_Vehicle.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_vehicles()