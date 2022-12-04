from scanner import *
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
    edit_config_list = Config().edit_configs()
    customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['Name'] is not None])
    list_of_config_customers = set(i[0] for i in edit_config_list)
    vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['SPZ'] is not None])
    list_of_config_vehicles = set()
    def __init__(self, **kwargs):
        super(Delete_Configs, self).__init__(**kwargs)
        for i in self.list_of_config_customers:
            btn = Button(text=i, size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_customer(self.customer_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
        mainbutton1 = Button(text='Vyber zakaznika', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        mainbutton2 = Button(text='Vyber vozidlo', size_hint=(.5, .25), pos=(60, 20))
        mainbutton2.bind(on_release=self.drop2.open)
        self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        self.btn1.bind(on_release=lambda btn: self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(mainbutton2)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)

    def set_customer(self, text):
        self.select_customer_id = text
        self.select_vehicle = None
        self.drop2.clear_widgets()
        self.drop2.select('Vyber vozidlo')
        self.list_of_config_vehicles = set(i[7] for i in self.edit_config_list if text == i[1])
        for i in self.list_of_config_vehicles:
            btn = Button(text=i, size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_vehicle(self.vehicle_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
            self.drop2.add_widget(btn)
    def set_vehicle(self, text):
        self.select_vehicle = text
        for i in  self.edit_config_list:
            if self.select_vehicle == i[8] and self.select_customer_id == i[1]:
                self.select_config_id = i[3]
                break
    def call_Back(self):
        App.get_running_app().stop()
    def check(self):
        if self.select_customer_id is None:
            self.notify.text = "Please select customer"
        elif self.select_vehicle is None:
            self.notify.text = "Please select SPZ"
        else:
            print(self.select_config_id)
            on_delete = Config().stiahni(self.select_config_id)
            on_delete.Customer_id = None
            on_delete.update()
            # on_delete.update()
            self.call_Back()


class Deleting(App):
    def build(self): return Delete_Configs()
