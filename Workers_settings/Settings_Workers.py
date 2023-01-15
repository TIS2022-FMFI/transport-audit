from Workers_settings.Delete_Workers import *
from Workers_settings.Add_Workers import *
from Workers_settings.Edit_Workers import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Workers (BoxLayout):
    screenManager = None

    def __init__(self, screenManager,**kwargs):
        super(Settings_Workers, self).__init__(**kwargs)
        self.screenManager = screenManager
    def call_add(self):
        self.screenManager.current
        self.screenManager.current = 'Add_Workers'
    def call_edit(self):
        self.screenManager.current = 'Edit_Workers'
    def call_delete(self):
        self.screenManager.current = 'Delete_Workers'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'


