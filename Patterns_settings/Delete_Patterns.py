from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer,Stillage_type,Pattern_Item,Pattern
class Delete_Patterns (BoxLayout):
    select_customer = None
    select_pattern  = None
    notify = Button(text = '')
    drop1 = DropDown()
    drop5 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    customer_list = dict([(i['Name'],i['id']) for i in Customer().vrat_vsetky() if i['Name'] is not None])
    pattern_list = dict([( i['id'],i['Customer_id']) for i in Pattern().vrat_vsetky() if i['Customer_id'] is not None])
    Edit_data = Pattern().Data_on_editing()
    def __init__(self, **kwargs):
        super(Delete_Patterns, self).__init__(**kwargs)
        for i in self.customer_list:
            if self.customer_list[i] in self.pattern_list.values():
                btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_customer_id(btn.text))
                btn.bind(on_release=lambda btn: self.drop5.select(btn.text))
                self.drop5.add_widget(btn)
        mainbutton1 = Button(text='Vyber pattern', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        mainbutton5 = Button(text='Customer', size_hint=(.5, .25), pos=(60, 20))
        mainbutton5.bind(on_release=self.drop5.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.drop5.bind(on_select=lambda instance, x: setattr(mainbutton5, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton5)
        self.add_widget(mainbutton1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def set_customer_id(self,tex1):
        self.select_pattern = None
        self.drop1.clear_widgets()
        self.drop1.select("Vyber pattern")
        self.select_customer = self.customer_list[tex1]
        list_of_patterns=[]
        for i in self.Edit_data:
            if i[1] == self.select_customer and i[3] not in list_of_patterns:
                list_of_patterns.append(i[3])
                btn = Button(text= i[3], size_hint_y=None, height=40, on_release=lambda btn: self.set_widgets(btn.text))
                btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
                self.drop1.add_widget(btn)
    def set_widgets(self,tex1):
        self.select_pattern = tex1
    def call_Back (self):
        App.get_running_app().stop()
    def check (self):
        if self.select_customer is None:
            self.notify.text = "Please choose customer"
        elif self.select_pattern is None:
            self.notify.text = "Please choose pattern"
        else:
            on_delete = Pattern().stiahni(self.select_pattern)
            on_delete.Customer_id = None
            on_delete.update()
            self.call_Back()
class Deleting (App):
    def build(self):return Delete_Patterns()