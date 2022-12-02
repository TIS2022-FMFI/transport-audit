from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer
class Add_Customers (BoxLayout):
    notify = Button(text = '')
    text1 = TextInput(text='Meno zakaznika')
    def __init__(self, **kwargs):
        super(Add_Customers, self).__init__(**kwargs)
        btn1 = Button(text="Pridaj")
        btn1.bind(on_release = lambda btn:self.check())
        btn2 = Button(text="Späť")
        btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(self.text1)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(self.notify)
    def call_Back (self):
        App.get_running_app().stop()
    def check (self):
        if  len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) == 0 or self.text1.text == "Meno zakaznika":
            self.notify.text = "Please enter a valid name."
        elif self.text1.text in [i['Name'] for i in Customer().vrat_vsetky()]:
            self.notify.text = "Name already exists"
        else:
            Customer().nahraj(self.text1.text)
            self.call_Back()
class Adding (App):
    def build(self):return Add_Customers()