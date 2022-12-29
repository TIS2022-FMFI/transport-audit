from Add_stillage_types import *
from Edit__stillage_types import *
from Delete_stillage_types import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Stillage_types (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Edituj")
    btn3 = Button(text="Vymaz")
    btn4 = Button(text="Spat")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Settings_Stillage_types, self).__init__(**kwargs)
        super().__init__()
        self.screenManager = screenManager
        self.btn1.bind(on_release = lambda btn: self.call_add())
        self.btn2.bind(on_release=lambda btn: self.call_edit())
        self.btn3.bind(on_release=lambda btn: self.call_delete())
        self.btn4.bind(on_release=lambda btn: self.call_back())
        self.add_widget(self.btn1)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)
    def call_add(self):
        self.screenManager.current = 'Add_Stillage_types'
    def call_edit(self):
        self.screenManager.current = 'Edit_Stillage_types'
    def call_delete(self):
        self.screenManager.current = 'Delete_Stillage_types'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'