from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer, Vehicle, User, Config, Advanced_user

class Edit_Configs(BoxLayout):
    select_config_id = None
    select_customer_id = None
    select_vehicle = None
    select_advanced_user = None
    on_delete_advanced_user = None
    notify = Button(text='')
    drop1 = DropDown()
    drop2 = DropDown()
    drop3 = DropDown()
    drop4 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    btn3 = Button(text="Pridaj polozku")
    btn4 = Button(text="Odstran polozku")
    edit_config_list = None
    customer_list = None
    list_of_config_customers = None
    vehicle_list = None
    workers_list = None
    list_of_config_vehicles = set()
    advanced_user_list = set()
    old_advanced_user_list = set()
    screenManager = None

    def __init__(self, screenManager,**kwargs):
        super(Edit_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton1 = Button(text='Vyber zakaznika', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        mainbutton2 = Button(text='Vyber vozidlo', size_hint=(.5, .25), pos=(60, 20))
        mainbutton2.bind(on_release=self.drop2.open)
        self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        mainbutton3 = Button(text='Vyber uzivatelov', size_hint=(.5, .25), pos=(60, 20))
        mainbutton3.bind(on_release=self.drop3.open)
        self.drop3.bind(on_select=lambda instance, x: setattr(mainbutton3, 'text', x))
        mainbutton4 = Button(text='Vybrati advanced users', size_hint=(.5, .25), pos=(60, 20))
        mainbutton4.bind(on_release=self.drop4.open)
        self.drop4.bind(on_select=lambda instance, x: setattr(mainbutton4, 'text', x))
        self.btn1.bind(on_release=lambda btn: self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.btn3.bind(on_release=lambda btn: self.check_adding_advanced_users())
        self.btn4.bind(on_release=lambda btn: self.check_deleted_advanced_user())
        self.add_widget(mainbutton1)
        self.add_widget(mainbutton2)
        self.add_widget(mainbutton3)
        self.add_widget(self.btn3)
        self.add_widget(mainbutton4)
        self.add_widget(self.btn4)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def synchronize_customers(self):
        self.select_customer_id = None
        self.edit_config_list = Config().edit_configs()
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.list_of_config_customers = set(i[0] for i in self.edit_config_list)
        self.drop1.clear_widgets()
        self.drop1.select("Vyber zakaznika")
        for i in self.list_of_config_customers:
            btn = Button(text=i, size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_customer(self.customer_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def synchronize_vehicles(self):
        self.select_vehicle = None
        self.vehicle_list = dict([(i['SPZ'], i['id']) for i in Vehicle().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.drop2.clear_widgets()
        self.drop2.select("Vyber vozidlo")
    def synchronize_workers(self):
        self.select_advanced_user = None
        self.workers_list = dict([(i['Name'][0] + ". " + i['Last_name'] + " " + str(i['code']),str(i['code'])) for i in User().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.advanced_user_list = set()
        self.old_advanced_user_list = set()
        self.drop3.clear_widgets()
        self.drop3.select("Vyber uzivatelov")
        for i in self.workers_list:
            btn = Button(text=i, size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_advance_user(btn.text))
            btn.bind(on_release=lambda btn: self.drop3.select(btn.text))
            self.drop3.add_widget(btn)
    def synchronize_configs(self):
        self.select_config_id = None
    def set_customer(self, text):
        self.select_customer_id = text
        self.select_vehicle = None
        self.drop2.clear_widgets()
        self.drop2.select('Vyber vozidlo')
        self.advanced_user_list = set()
        self.synchronize_choosed_advanced_users()
        self.list_of_config_vehicles = set(i[11] for i in self.edit_config_list if text == i[1])
        for i in self.list_of_config_vehicles:
            btn = Button(text=i, size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_vehicle(self.vehicle_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
            self.drop2.add_widget(btn)
    def set_vehicle(self, text):
        self.select_vehicle = text
        for i in  self.edit_config_list:
            if self.select_vehicle == i[7] and self.select_customer_id == i[1]:
                self.select_config_id = i[5]
                break
        self.advanced_user_list= set([User().stiahni(i['User_code']).Name[0] + ". " + User().stiahni(i['User_code']).Last_name + " " + str(i['User_code']) for i in Advanced_user().vrat_vsetky() if i['doplnok'] != 'DELETED' and i['Config_id'] == self.select_config_id])
        self.old_advanced_user_list = set([User().stiahni(i['User_code']).Name[0] + ". " + User().stiahni(i['User_code']).Last_name + " " + str(i['User_code']) for i in Advanced_user().vrat_vsetky() if i['doplnok'] != 'DELETED' and i['Config_id'] == self.select_config_id])
        self.synchronize_choosed_advanced_users()

    def set_advance_user(self, text):
        self.select_advanced_user = text

    def synchronize_choosed_advanced_users(self):
        self.drop4.clear_widgets()
        self.drop4.select('Vybrati advanced_users')
        for i in self.advanced_user_list:
            btn = Button(text=str(i), size_hint_y=None, height=40,
                         on_release=lambda btn: self.set_on_delete_advanced_user(btn.text))
            btn.bind(on_release=lambda btn: self.drop4.select(btn.text))
            self.drop4.add_widget(btn)

    def check_adding_advanced_users(self):
        if self.select_advanced_user is None:
            self.notify.text = "Please choose advanced user you want add"
        else:
            self.advanced_user_list.add(self.select_advanced_user)
            self.synchronize_choosed_advanced_users()
            self.select_advanced_user = None
            self.drop3.select("Vyber uzivatelov")
            self.on_delete_advanced_user = None

    def check_deleted_advanced_user(self):
        if self.on_delete_advanced_user is None:
            self.notify.text = "Please select item to delete"
        else:
            self.advanced_user_list.remove(self.on_delete_advanced_user)
            self.synchronize_choosed_advanced_users()
            self.on_delete_advanced_user = None
    def call_Back(self):
        self.screenManager.current = 'Settings_Configs'

    def set_on_delete_advanced_user(self, text):
        self.on_delete_advanced_user = text

    def check(self):
        if self.select_customer_id is None:
            self.notify.text = "Please select customer"
        elif self.select_vehicle is None:
            self.notify.text = "Please select SPZ"
        elif len(self.advanced_user_list) == 0:
            self.notify.text = "Please select advanced user you want to add"
        else:
            for i in Advanced_user().vrat_vsetky():
                if i['Config_id'] == self.select_config_id and i['doplnok'] != 'DELETED':
                    on_edit_advanced_user = User().stiahni(i['User_code'])
                    on_checking_edit_advanced_user = on_edit_advanced_user.Name[0] + ". " + on_edit_advanced_user.Last_name + " " + str(on_edit_advanced_user.code)
                    if on_checking_edit_advanced_user in self.old_advanced_user_list and on_checking_edit_advanced_user in self.advanced_user_list:
                        self.advanced_user_list.remove(on_checking_edit_advanced_user)
                    elif on_checking_edit_advanced_user in self.old_advanced_user_list and on_checking_edit_advanced_user not in self.advanced_user_list:
                        on_delete_advqanced_user = Advanced_user().stiahni(i['id'])
                        on_delete_advqanced_user.zmazat()
            for i in self.advanced_user_list:
                Advanced_user().nahraj(self.select_config_id,self.workers_list[i])
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""

        self.on_delete_advanced_user = None
        self.drop4.clear_widgets()
        self.drop4.select("Vybrati advanced users")

        self.synchronize_customers()
        self.synchronize_vehicles()
        self.synchronize_workers()
        self.synchronize_configs()