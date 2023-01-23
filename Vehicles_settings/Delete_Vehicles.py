from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Vehicle
class Delete_Vehicles (BoxLayout):
    """
    mazanie SPZ
    """
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaž")
    btn2 = Button(text="Späť")
    vehicle_list = None
    screenManager = None
    values=[]
    def synchronize_vehicles(self):
        """
        nacita SPZ z databazy
        """
        self.on_delete_selected = None
        self.values = []
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.vehicle_list:
            self.values.append(i)
        self.ids.spinner_delete_vehicle.values = self.values
        self.ids.spinner_delete_vehicle.text = "Vyber vozidlo na vymazanie"
    def __init__(self,screenManager, **kwargs):
        super(Delete_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
    def select_id(self,tex):
        """
        oznaci SPZ na vymazanie
        """
        if tex not in self.vehicle_list:
            return
        self.on_delete_selected  = self.vehicle_list[tex]
    def call_Back (self):
        """
        presunutie sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Vehicles'
    def check (self):
        """
        kontrola vstupov nasledne mazanie SPZ
        """
        if (self.on_delete_selected is None):
                self.notify.text = "Nie je vybraté vozidlo."
        else:
            on_delete_Vehicle = Vehicle().stiahni(self.on_delete_selected)
            on_delete_Vehicle.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        """
        prvotna inicializacia obrazovky
        """
        self.notify.text = ""
        self.synchronize_vehicles()