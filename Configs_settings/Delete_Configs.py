from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer, Vehicle, User, Config, Advanced_user

class Delete_Configs(BoxLayout):
    select_config_id = None
    select_customer_id = None
    select_vehicle = None
    notify = Button(text='')
    drop1 = DropDown()
    drop2 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    edit_config_list = None
    customer_list = None
    list_of_config_customers = None
    vehicle_list = None
    list_of_config_vehicles = set()
    screenManager = None
    values1=[]
    values2=[]
    def __init__(self, screenManager,**kwargs):
        super(Delete_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
        # mainbutton1 = Button(text='Vyber zakaznika', size_hint=(.5, .25), pos=(60, 20))
        # mainbutton1.bind(on_release=self.drop1.open)
        # self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        # mainbutton2 = Button(text='Vyber vozidlo', size_hint=(.5, .25), pos=(60, 20))
        # mainbutton2.bind(on_release=self.drop2.open)
        # self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        # self.btn1.bind(on_release=lambda btn: self.check())
        # self.btn2.bind(on_release=lambda btn: self.call_Back())
        # self.add_widget(mainbutton1)
        # self.add_widget(mainbutton2)
        # self.add_widget(self.btn1)
        # self.add_widget(self.btn2)
        # self.add_widget(self.notify)

    def synchronize_customers(self):
        self.select_customer_id = None
        self.edit_config_list = Config().edit_configs()
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.list_of_config_customers = set(i[0] for i in self.edit_config_list)
        # self.drop1.clear_widgets()
        self.values1 = []
        # self.drop1.select("Vyber zakaznika")
        for i in self.list_of_config_customers:
            # btn = Button(text=i, size_hint_y=None, height=40,on_release=lambda btn: self.set_customer(self.customer_list[btn.text]))
            # btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            # self.drop1.add_widget(btn)
            self.values1.append(i)
        self.ids.spinner_delete_config1.values = self.values1
    def synchronize_vehicles(self):
        self.select_vehicle = None
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.drop2.clear_widgets()
        self.drop2.select("Vyber vozidlo")
    #     pripadne config vehicle list vycistit ale nemalo by vadit
    def synchronize_configs(self):
        self.select_config_id = None
    def set_customer(self, text1):
        text = self.customer_list[text1]
        self.select_customer_id = text
        self.select_vehicle = None
        # self.drop2.clear_widgets()
        self.values2=[]
        # self.drop2.select('Vyber vozidlo')
        self.list_of_config_vehicles = set(i[11] for i in self.edit_config_list if text == i[1])
        for i in self.list_of_config_vehicles:
            # btn = Button(text=i, size_hint_y=None, height=40,on_release=lambda btn: self.set_vehicle(self.vehicle_list[btn.text]))
            # btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
            # self.drop2.add_widget(btn)
            self.values2.append(i)
        self.ids.spinner_delete_config2.values = self.values2
    def set_vehicle(self, text1):
        text = self.vehicle_list[text1]
        self.select_vehicle = text
        for i in self.edit_config_list:
            if self.select_vehicle == i[7] and self.select_customer_id == i[1]:
                self.select_config_id = i[5]
                break
    def call_Back(self):
        self.screenManager.current = 'Settings_Configs'
    def check(self):
        if self.select_customer_id is None:
            self.notify.text = "Please select customer"
        elif self.select_vehicle is None:
            self.notify.text = "Please select SPZ"
        else:
            on_delete = Config().stiahni(self.select_config_id)
            on_delete.zmazat()
            self.call_Back()

    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_customers()
        self.synchronize_vehicles()
        self.synchronize_configs()