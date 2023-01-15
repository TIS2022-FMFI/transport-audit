#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer
class Add_Customers (BoxLayout):
    notify = Button(text = '')
    text1 = TextInput(text='Meno zákazníka')
    screenManager = None
    customer_list = None
    def __init__(self,screenManager, **kwargs):
        super(Add_Customers, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_add_customer
        self.notify = self.ids.notify
    def synchronize_customers(self):
        self.customer_list = [i['Name'] for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def call_Back (self):
        self.screenManager.current = 'Settings_Customers'
    def check (self):
        if  len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) == 0 or self.text1.text == "Meno zákazníka":
            self.notify.text = "Zadaj názov"
        elif self.text1.text in self.customer_list:
            self.notify.text = "Zákaznik už existuje"
        else:
            Customer().nahraj(self.text1.text)
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.text1.text = ''
        self.synchronize_customers()