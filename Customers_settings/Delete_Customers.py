#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer
class Delete_Customers (BoxLayout):
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaž")
    btn2 = Button(text="Späť")
    customer_list = None
    screenManager = None
    values=[]
    def synchronize_customers(self):
        self.on_delete_selected = None
        self.values = []
        self.customer_list = dict([(i['Name'],i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            self.values.append(i)
        self.ids.spinner_delete_customer.values = self.values
        self.ids.spinner_delete_customer.text = "Vyber pracovníka na vymazanie"
    def __init__(self, screenManager,**kwargs):
        super(Delete_Customers, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
    def select_code(self,tex):
        if tex not in self.customer_list:
            return
        self.on_delete_selected = self.customer_list[tex]
    def call_Back (self):
        self.screenManager.current = 'Settings_Customers'
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Vyber zákazníka"
        else:
            on_delete_customer = Customer().stiahni(self.on_delete_selected)
            on_delete_customer.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_customers()