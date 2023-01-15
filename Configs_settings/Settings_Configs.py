from Configs_settings.Delete_Configs import *
from Configs_settings.Add_Configs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Configs (BoxLayout):
    btn1 = Button(text="Pridaj")
    btn3 = Button(text="Vymaž")
    btn4 = Button(text="Späť")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Settings_Configs, self).__init__(**kwargs)
        self.screenManager = screenManager
    def call_add(self):
        self.screenManager.current = 'Add_Configs'

    def call_delete(self):
        self.screenManager.current = 'Delete_Configs'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'