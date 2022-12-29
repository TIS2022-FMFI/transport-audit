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
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    customer_list = None
    screenManager = None
    values=[]
    def synchronize_customers(self):
        self.on_delete_selected = None
        self.customer_list = dict([(i['Name'],i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        # self.drop1.clear_widgets()
        # self.drop1.select("Vyber pracovnika na vymazanie")
        for i in self.customer_list:
            # btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.select_code(btn.text))
            # btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            # self.drop1.add_widget(btn)
            self.values.append(i)
        self.ids.spinner_delete_customer.values = self.values
    def __init__(self, screenManager,**kwargs):
        super(Delete_Customers, self).__init__(**kwargs)
        self.screenManager = screenManager
        # mainbutton1 = Button(text='Vyber pracovnika na vymazanie', size_hint=(.5, .25), pos=(60, 20))
        # mainbutton1.bind(on_release=self.drop1.open)
        # self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        # self.btn1.bind(on_release = lambda btn:self.check())
        # self.btn2.bind(on_release=lambda btn: self.call_Back())
        # self.add_widget(mainbutton1)
        # self.add_widget(self.btn1)
        # self.add_widget(self.btn2)
        # self.add_widget(self.notify)
    def select_code(self,tex):
        self.on_delete_selected = self.customer_list[tex]
    def call_Back (self):
        self.screenManager.current = 'Settings_Customers'
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Please choose Customer by code you want delete."
        else:
            on_delete_customer = Customer().stiahni(self.on_delete_selected)
            on_delete_customer.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_customers()