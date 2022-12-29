from Workers_settings.Settings_Workers import *
from Customers_settings.Settings_Customers import *
from Vehicles_settings.Settings_Vehicles import *
from Configs_settings.Settings_Configs import *
from Stillage_types_settings.Settings_Stillage_types import *
from Export_setting.Settings_export import *
from Patterns_settings.Settings_Patterns import *

from sqlite import User_Role, User
from random import randint
class Menu_screen (BoxLayout):
    btn1 = Button(text="Zamestnanci")
    btn2 = Button(text="Zakaznici")
    btn3 = Button(text="Vozidla")
    btn4 = Button(text="Configy")
    btn5 = Button(text="Patterny")
    btn6 = Button(text="Export settings")
    btn7 = Button(text = "Typy vozikov")
    btnOdhlasenie = Button(text="Odhlasit")
    btnAudit = Button(text="Zacat audit")
    screenManager = None
    def __init__(self,aplikacia, povodna, auditScreen, **kwargs):
        super(Menu_screen, self).__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.auditScreen = auditScreen
        self.screenManager = aplikacia.screenManager
        self.btn1 = self.ids.MSbtn1
        self.btn2 = self.ids.MSbtn2
        self.btn3 = self.ids.MSbtn3
        self.btn4 = self.ids.MSbtn4
        self.btn5 = self.ids.MSbtn5
        self.btn6 = self.ids.MSbtn6
        self.btn7 = self.ids.MSbtn7

        self.btnOdhlasenie = self.ids.MSbtn7
        # self.btn1.bind(on_release=lambda btn:self.call_Workers_settings())
        # self.btn2.bind(on_release=lambda btn: self.call_Customers_settings())
        # self.btn3.bind(on_release=lambda btn: self.call_Vehicles_settings())
        # self.btn4.bind(on_release=lambda btn: self.call_Configs_settings())
        # self.btn5.bind(on_release=lambda btn: self.call_Patterns_settings())
        # self.btn6.bind(on_release=lambda btn: self.call_Exportss_settings())
        # self.btnOdhlasenie.bind(on_release=self.odhlasit)
        # self.btnAudit.bind(on_release=self.zacatAudit)

    def vytvorMenu(self, *arg):

        # self.clear_widgets()
        # id  = self.aplikacia.zamestnanec.User_Role_id
        # rola = User_Role().stiahni(id).name

        # mnou dorobene docasne
        rola = 'Administrátor'
        id = '0f32fe18-0407-338b-dbd2-b8336b563381'
        # ignorovat

        # ----------------------------
        print("rola : ", rola)


        # if rola == 'Administrátor':
        #     self.add_widget(self.btn1)
        # if rola in {'Administrátor', 'Operátor'}:
        #     self.add_widget(self.btn2)
        #     self.add_widget(self.btn3)
        #     self.add_widget(self.btn4)
        #     self.add_widget(self.btn5)
        #     self.add_widget(self.btn6)
        # self.add_widget(self.btnOdhlasenie)
        # self.add_widget(self.btnAudit)

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
    def call_Stillage_types_settings(self):
        self.screenManager.current = 'Settings_Stillage_types'
    def call_Exportss_settings(self):
        self.screenManager.current = 'Settings_Exports'
    def zacatAudit(self, *args):
        self.aplikacia.screenManager.current = self.auditScreen

    def odhlasit(self, *args):
        self.aplikacia.zamestnanec = None
        self.povodna.kodZamestnanca.clear()
        self.aplikacia.screenManager.current = self.povodna.name

