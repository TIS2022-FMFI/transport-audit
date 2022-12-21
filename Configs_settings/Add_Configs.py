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
    def __init__(self, screenManager,**kwargs):
        super(Add_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton1 = Button(text='Vyber zakaznika', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        mainbutton2 = Button(text='Vyber vozidlo', size_hint=(.5, .25), pos=(60, 20))
        mainbutton2.bind(on_release=self.drop2.open)
        self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(mainbutton2)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def synchronize_customers(self):
        self.select_customer_id  = None
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.drop1.clear_widgets()
        self.drop1.select("Vyber zakaznika")
        for i in self.customer_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_customer(self.customer_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def synchronize_vehicles(self):
        self.select_vehicle = None
        self.advanced_user_list = set()
        self.drop2.clear_widgets()
        self.drop2.select("Vyber vozidlo")
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        print(self.vehicle_list)
        for i in self.vehicle_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_vehicle(self.vehicle_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
            self.drop2.add_widget(btn)

    def synchronize_configs(self):
        self.config_list = [(i["Customer_id"], i["Vehicle_id"]) for i in Config().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def set_customer(self,text):
        self.select_customer_id=text
    def set_vehicle(self,text):
        self.select_vehicle = text

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
            Config().nahraj(self.select_customer_id,self.select_vehicle)
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_customers()
        self.synchronize_vehicles()
        self.synchronize_configs()