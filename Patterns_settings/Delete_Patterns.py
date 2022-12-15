from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer,Stillage_type,Pattern_Item,Pattern
class Delete_Patterns (BoxLayout):
    select_customer = None
    select_pattern  = None
    notify = Button(text = '')
    drop2 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    customer_list = None
    pattern_list = None
    Edit_data = None
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Delete_Patterns, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton2 = Button(text='Customer', size_hint=(.5, .25), pos=(60, 20))
        mainbutton2.bind(on_release=self.drop2.open)
        self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton2)
        # self.add_widget(mainbutton1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)

    def synchronize_customers(self):
        self.select_customer = None
        self.drop2.clear_widgets()
        self.drop2.select("Customer")
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            if self.customer_list[i] in self.pattern_list.values():
                btn = Button(text=i, size_hint_y=None, height=40, on_release=lambda btn: self.set_customer_id(btn.text))
                btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
                self.drop2.add_widget(btn)
    def synchronize_patterns(self):
        self.select_pattern = None
        self.pattern_list = dict([(i['id'], i['Customer_id']) for i in Pattern().vrat_vsetky() if i['doplnok'] != 'DELETED'])
    def set_customer_id(self,tex1):
        self.select_pattern = None
        self.select_customer = self.customer_list[tex1]
        for i in Pattern().vrat_vsetky():
            if i['doplnok'] != 'DELETED' and i['Customer_id'] == self.select_customer:
                self.select_pattern = i['id']
                break
    def call_Back (self):
        self.screenManager.current = 'Settings_Patterns'
    def check (self):
        if self.select_customer is None:
            self.notify.text = "Please choose customer"
        else:
            on_delete = Pattern().stiahni(self.select_pattern)
            on_delete.zmazat()
            for i in Pattern_Item().vrat_vsetky():
                on_delete_pattern_item = Pattern_Item().stiahni(i['id'])
                if on_delete_pattern_item.Pattern_id == on_delete.id:
                    on_delete_pattern_item.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_patterns()
        self.synchronize_customers()
        self.Edit_data = Pattern().Data_on_editing()