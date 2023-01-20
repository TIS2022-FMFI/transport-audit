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
    btn1 = Button(text="Vymaž")
    btn2 = Button(text="Späť")
    customer_list = None
    pattern_list = None
    Edit_data = None
    screenManager = None
    values=[]
    def __init__(self,screenManager, **kwargs):
        super(Delete_Patterns, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify

    def synchronize_customers(self):
        self.select_customer = None
        # self.drop2.clear_widgets()
        # self.drop2.select("Customer")
        self.values = []
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            if self.customer_list[i] in self.pattern_list.values():
                self.values.append(i)
        self.ids.spinner_delete_patter.values = self.values
        self.ids.spinner_delete_patter.text = "Zákazník"
    def synchronize_patterns(self):
        self.select_pattern = None
        self.pattern_list = dict([(i['id'], i['Customer_id']) for i in Pattern().vrat_vsetky() if i['doplnok'] != 'DELETED'])
    def set_customer_id(self,tex1):
        self.select_pattern = None
        if tex1 not in self.customer_list:
            return
        self.select_customer = self.customer_list[tex1]
        for i in Pattern().vrat_vsetky():
            if i['doplnok'] != 'DELETED' and i['Customer_id'] == self.select_customer:
                self.select_pattern = i['id']
                break
    def call_Back (self):
        self.screenManager.current = 'Settings_Patterns'
    def check (self):
        if self.select_customer is None:
            self.notify.text = "Vyber zákazníka"
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