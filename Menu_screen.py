from Workers_settings.Settings_Workers import *
from Customers_settings.Settings_Customers import *
from Vehicles_settings.Settings_Vehicles import *
from Configs_settings.Settings_Configs import *
from Patterns_settings.Settings_Patterns import *
class Menu_screen (BoxLayout):
    btn1 = Button(text="Zamestnanci")
    btn2 = Button(text="Zakaznici")
    btn3 = Button(text="Vozidla")
    btn4 = Button(text="Configy")
    btn5 = Button(text="Patterny")
    btn6 = Button(text="Odhlasit")
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        super(Menu_screen, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.btn1.bind(on_release=lambda btn:self.call_Workers_settings())
        self.btn2.bind(on_release=lambda btn: self.call_Customers_settings())
        self.btn3.bind(on_release=lambda btn: self.call_Vehicles_settings())
        self.btn4.bind(on_release=lambda btn: self.call_Configs_settings())
        self.btn5.bind(on_release=lambda btn: self.call_Patterns_settings())
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.btn3)
        self.add_widget(self.btn4)
        self.add_widget(self.btn5)
        self.add_widget(self.btn6)
    def call_Workers_settings(self):
        self.screenManager.current = 'Settings_Workers'
    def call_Customers_settings(self):
        self.screenManager.current = 'Settings_Customers'
    def call_Vehicles_settings(self):
        self.screenManager.current = 'Settings_Vehicles'
    def call_Configs_settings(self):
        self.screenManager.current = 'Settings_Configs'
    def call_Patterns_settings(self):
        self.screenManager.current = 'Settings_Patterns'