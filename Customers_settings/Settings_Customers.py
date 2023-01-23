from Customers_settings.Delete_Customers import *
from Customers_settings.Add_Customers import *
from Customers_settings.Edit_Customers import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
class Settings_Customers (BoxLayout):

    screenManager = None
    def __init__(self,screenManager, **kwargs):
        """
        nastavenia zakaznikov
        nasledovne funkcie zavolaju prislusny screen ktory si vyberieme
        """
        super(Settings_Customers, self).__init__(**kwargs)
        self.screenManager = screenManager
    def call_add(self):
        self.screenManager.current = 'Add_Customers'
    def call_edit(self):
        self.screenManager.current = 'Edit_Customers'
    def call_delete(self):
        self.screenManager.current = 'Delete_Customers'
    def call_back(self):
        self.screenManager.current = 'Menu_screen'