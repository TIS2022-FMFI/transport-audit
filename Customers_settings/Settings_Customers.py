from Customers_settings.Delete_Customers import *
from Customers_settings.Add_Customers import *
from Customers_settings.Edit_Customers import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Customers (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Uprav")
    btn3 = Button(text="Vymaz")
    btn4 = Button(text="Spat")
    def __init__(self, **kwargs):
        super(Settings_Customers, self).__init__(**kwargs)
        super().__init__()
        self.btn1.bind(on_release = lambda btn: self.call_add())
        self.btn2.bind(on_release=lambda btn: self.call_edit())
        self.btn3.bind(on_release=lambda btn: self.call_delete())
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)
    def call_add(self):
        App.get_running_app().stop()
        Adding().run()
    def call_edit(self):
        App.get_running_app().stop()
        Editing().run()
    def call_delete(self):
        App.get_running_app().stop()
        Deleting().run()
class Zakaznici (App):
    def build(self):return Settings_Customers()

