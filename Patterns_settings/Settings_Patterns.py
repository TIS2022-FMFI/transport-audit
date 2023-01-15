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
    def call_add(self):
        self.screenManager.current = 'Add_Patterns'
    def call_edit(self):
        self.screenManager.current = 'Edit_Patterns'
    def call_delete(self):
        self.screenManager.current = 'Delete_Patterns'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'