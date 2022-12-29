from Customers_settings.Delete_Customers import *
from Customers_settings.Add_Customers import *
from Customers_settings.Edit_Customers import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Customers (BoxLayout):
    # btn1 = Button(text="Pridaj")
    # btn2 = Button(text="Uprav")
    # btn3 = Button(text="Vymaz")
    # btn4 = Button(text="Spat")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Settings_Customers, self).__init__(**kwargs)
        # super().__init__()
        self.screenManager = screenManager
        # self.btn1.bind(on_release = lambda btn: self.call_add())
        # self.btn2.bind(on_release=lambda btn: self.call_edit())
        # self.btn3.bind(on_release=lambda btn: self.call_delete())
        # self.btn4.bind(on_release=lambda btn: self.call_back())
        # self.add_widget(self.btn1)
        # self.add_widget(self.btn2)
        # self.add_widget(self.btn3)
        # self.add_widget(self.btn4)
    def call_add(self):
        self.screenManager.current = 'Add_Customers'
    def call_edit(self):
        self.screenManager.current = 'Edit_Customers'
    def call_delete(self):
        self.screenManager.current = 'Delete_Customers'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'