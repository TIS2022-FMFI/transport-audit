from Patterns_settings.Delete_Patterns import *
from Patterns_settings.Add_Patterns import *
from Patterns_settings.Edit_Patterns import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Patterns (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Uprav")
    btn3 = Button(text="Vymaz")
    btn4 = Button(text="Spat")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        self.screenManager = screenManager
        super(Settings_Patterns, self).__init__(**kwargs)
        super().__init__()
        self.btn1.bind(on_release = lambda btn: self.call_add())
        self.btn2.bind(on_release=lambda btn: self.call_edit())
        self.btn3.bind(on_release=lambda btn: self.call_delete())
        self.btn4.bind(on_release=lambda btn: self.call_back())
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)
    def call_add(self):
        self.screenManager.current = 'Add_Patterns'
    def call_edit(self):
        self.screenManager.current = 'Edit_Patterns'
    def call_delete(self):
        self.screenManager.current = 'Delete_Patterns'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'