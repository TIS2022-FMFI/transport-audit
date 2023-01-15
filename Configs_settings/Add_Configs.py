from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from sqlite import Customer,Vehicle, Config
class Add_Configs (BoxLayout):
    select_customer_id  = None
    select_vehicle = None
    notify = Button(text = '')
    drop1 = DropDown()
    drop2 = DropDown()
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Späť")
    customer_list = None
    vehicle_list = None
    config_list =None
    screenManager = None
    values1 = []
    values2 = []
    def __init__(self, screenManager,**kwargs):
        super(Add_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
    def synchronize_customers(self):
        self.select_customer_id  = None
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.values1 = []
        for i in self.customer_list:
            self.values1.append(i)
        self.ids.spinner_add_config1.values = self.values1
        self.ids.spinner_add_config1.text = "Vyber zakaznika"
    def synchronize_vehicles(self):
        self.select_vehicle = None
        self.advanced_user_list = set()
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        print(self.vehicle_list)
        self.values2 = []
        for i in self.vehicle_list:
            self.values2.append(i)
        self.ids.spinner_add_config2.values = self.values2
        self.ids.spinner_add_config2.text = "Vyber SPZ"
    def synchronize_configs(self):
        self.config_list = [(i["Customer_id"], i["Vehicle_id"]) for i in Config().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def set_customer(self,text):
        if text != "Vyber zakaznika":
            self.select_customer_id = self.customer_list[text]
    def set_vehicle(self,text):
        if text != "Vyber SPZ":
            self.select_vehicle = self.vehicle_list[text]

    def call_Back (self):
        self.screenManager.current = 'Settings_Configs'

    def set_on_delete_advanced_user(self,text):
        self.on_delete_advanced_user = text
    def check (self):
        if self.select_customer_id is None:
            self.notify.text = "Please select customer"
        elif self.select_vehicle is None:
            self.notify.text = "Please select SPZ"
        elif (self.select_customer_id,self.select_vehicle) in self.config_list:
            self.notify.text = "This config with these SPZ and customer already exists"
        else:
            print(self.select_customer_id, self.select_vehicle)
            Config().nahraj(self.select_customer_id,self.select_vehicle)
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_customers()
        self.synchronize_vehicles()
        self.synchronize_configs()