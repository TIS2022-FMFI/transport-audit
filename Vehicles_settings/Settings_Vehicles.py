from Vehicles_settings.Delete_Vehicles import *
from Vehicles_settings.Add_Vehicles import *
from Vehicles_settings.Edit_Vehicles import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Vehicles (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Uprav")
    btn3 = Button(text="Vymaz")
    btn4 = Button(text="Spat")
    screenManager = None
    def __init__(self, screenManager,**kwargs):
        super(Settings_Vehicles, self).__init__(**kwargs)
        self.screenManager = screenManager
    def call_add(self):
        self.screenManager.current = 'Add_Vehicles'
    def call_edit(self):
        self.screenManager.current = 'Edit_Vehicles'
    def call_delete(self):
        self.screenManager.current = 'Delete_Vehicles'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'

