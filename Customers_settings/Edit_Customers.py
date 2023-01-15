#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer
class Edit_Customers (BoxLayout):
    select_id  = None
    notify = Button(text = '')
    text1 = TextInput(text='Meno')
    drop1 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    customer_list = None
    screenManager = None
    values = []
    def synchronize_customers(self):
        self.select_id = None
        self.values = []
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            self.values.append(i)
        self.ids.spinner_edit_customer.values = self.values
        self.ids.spinner_edit_customer.text = "Vyber zakaznika na úpravu"
    def __init__(self,screenManager, **kwargs):
        super(Edit_Customers, self).__init__(**kwargs)        
        self.screenManager = screenManager
        self.notify = self.ids.notify
        self.text1 = self.ids.text_customer
    def set_widgets(self,tex1):
        if tex1 not in self.customer_list:
            return
        self.text1.text = tex1
        self.select_id = self.customer_list[tex1]
    def call_Back (self):
        self.screenManager.current = 'Settings_Customers'
    def check (self):
        if (self.select_id is None):
                self.notify.text = "Vyber zákazníka"
        elif self.text1.text in self.customer_list.keys() and self.customer_list[self.text1.text] != self.select_id:
            self.notify.text = "Zákazník už existuje"
        elif len([x for x in self.text1.text if((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) == 0 or self.text1.text == "Vyber zákazníka na úpravu":
            self.notify.text = "Zadaj názov"
        else:
            updated_customer = Customer().stiahni(self.select_id)
            updated_customer.Name = self.text1.text
            updated_customer.update()
            self.call_Back()
    def clear_screen(self, *args):
        self.synchronize_customers()
        self.text1.text = ""
        self.notify.text = ""