from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer, Vehicle, Config

class Delete_Configs(BoxLayout):
    """
    mazanie configov
    """
    select_config_id = None
    select_customer_id = None
    select_vehicle = None
    notify = Button(text='')
    drop1 = DropDown()
    drop2 = DropDown()
    btn1 = Button(text="Vymaž")
    btn2 = Button(text="Späť")
    edit_config_list = None
    customer_list = None
    list_of_config_customers = None
    vehicle_list = None
    list_of_config_vehicles = set()
    screenManager = None
    values1 = []
    values2 = []
    def __init__(self, screenManager,**kwargs):
        super(Delete_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify

    def synchronize_customers(self):
        """
        nacita zakaznikov z databazy
        """
        self.select_customer_id = None
        self.edit_config_list = Config().edit_configs()
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.list_of_config_customers = set(i[0] for i in self.edit_config_list)
        self.values1 = []
        self.ids.spinner_delete_config1.values = self.values1
        for i in self.list_of_config_customers:
            self.values1.append(i)
        self.ids.spinner_delete_config1.values = self.values1
        self.ids.spinner_delete_config1.text = "Vyber zákazníka"
    def synchronize_vehicles(self):
        """
        nacita SPZ z databazy
        """
        self.select_vehicle = None
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.values2 = []
        self.ids.spinner_delete_config2.values = self.values2
        self.ids.spinner_delete_config2.text = "Vyber vozidlo"
    def synchronize_configs(self):
        """
        nacita configy z databazy
        """
        self.select_config_id = None
    def set_customer(self, text1):
        """
        vybrateho zakaznika ulozi zaroven nacita zaroven natiahne zoznam SPZ ktore obsahuju konfigy s vybratym zakaznikom
        """
        if text1 not in self.customer_list:
            return
        text = self.customer_list[text1]
        self.select_customer_id = text
        self.select_vehicle = None
        self.values2 = []
        self.ids.spinner_delete_config2.values = self.values2
        self.list_of_config_vehicles = set(i[11] for i in self.edit_config_list if text == i[1])
        for i in self.list_of_config_vehicles:
            self.values2.append(i)
        self.ids.spinner_delete_config2.values = self.values2
        self.ids.spinner_delete_config2.text = "Vyber vozidlo"
    def set_vehicle(self, text1):
        """
        ulozenie SPZ vybratej a najdenie prislusneho configu
        """
        if text1 not in self.vehicle_list:
            return
        text = self.vehicle_list[text1]
        self.select_vehicle = text
        for i in self.edit_config_list:
            if self.select_vehicle == i[7] and self.select_customer_id == i[1]:
                self.select_config_id = i[5]
                break
    def call_Back(self):
        """
        presunutie sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Configs'
    def check(self):
        """
        kontrola vstupov nasledne mazanie konfigu
        """
        if self.select_customer_id is None:
            self.notify.text = "Vyber zákazníka"
        elif self.select_vehicle is None:
            self.notify.text = "Vyber ŠPZ"
        else:
            on_delete = Config().stiahni(self.select_config_id)
            on_delete.zmazat()
            self.call_Back()

    def clear_screen(self, *args):
        """
        prvotna inicializacia obrazovky
        """
        self.notify.text = ""
        self.synchronize_customers()
        self.synchronize_vehicles()
        self.synchronize_configs()