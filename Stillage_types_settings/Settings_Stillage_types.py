from Stillage_types_settings.Add_stillage_types import *
from Stillage_types_settings.Edit__stillage_types import *;
from Stillage_types_settings.Delete_stillage_types import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Stillage_types (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Uprav")
    btn3 = Button(text="Vymaž")
    btn4 = Button(text="Späť")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Settings_Stillage_types, self).__init__(**kwargs)
        self.screenManager = screenManager
    def call_add(self):
        self.screenManager.current = 'Add_Stillage_types'
    def call_edit(self):
        self.screenManager.current = 'Edit_Stillage_types'
    def call_delete(self):
        self.screenManager.current = 'Delete_Stillage_types'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'