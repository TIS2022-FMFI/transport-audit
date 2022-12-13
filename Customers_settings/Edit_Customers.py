from scanner import *
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
    def synchronize_customers(self):
        self.select_id = None
        self.drop1.clear_widgets()
        self.drop1.select("Vyber zakaznika na upravu")
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_widgets(btn.text))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def __init__(self,screenManager, **kwargs):
        super(Edit_Customers, self).__init__(**kwargs)        
        self.screenManager = screenManager
        mainbutton1 = Button(text='Vyber zakaznika na upravu', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())        
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(self.text1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def set_widgets(self,tex1):
        self.text1.text = tex1
        self.select_id = self.customer_list[tex1]
    def call_Back (self):
        self.screenManager.current = 'Settings_Customers'
    def check (self):
        if (self.select_id is None):
                self.notify.text = "Please choose customer by code you want edit."
        elif self.text1.text in self.customer_list.keys() and self.customer_list[self.text1.text] != self.select_id:
            self.notify.text = "This customer already exists"
        elif len([x for x in self.text1.text if((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) == 0 or self.text1.text == "Vyber zakaznika na upravu":
            self.notify.text = "Please enter a valid first name."
        else:
            updated_customer = Customer().stiahni(self.select_id)
            updated_customer.Name = self.text1.text
            updated_customer.update()
            self.call_Back()
    def clear_screen(self, *args):
        self.text1.text = "Meno"
        self.notify.text = ""
        self.synchronize_customers()