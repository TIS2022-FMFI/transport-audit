from kivy.lang import Builder

from Menu_screen import *
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from startScreen2 import StartScreen
from UzavretyAudit import UzavretyKamion
from priebehAuditu import PrebiehajuciAudit

from auditUvod import UvodAuditu
from kivy.utils import platform
if platform == "android": # Zarucuje, že iba na androide sa if spustí, teda android package sa nemusí (a ani nedá) inštalovať
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,Permission.CAMERA])

from sqlite import synchronize_db_server_client
try:
    synchronize_db_server_client()
except:
    print("neda sa pripojit")
    pass
from skener2 import Scanner as Scanner2

class MainApp(App):
    def build(self):
        if platform == "android":
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])
        Builder.load_file('design.kv')
        #Vehicle().stiahni('9a414a42-1edc-42dc-a562-e635de6db7d2').zmazat()
        self.sm = self.screenManager = ScreenManager()
        # Configs
        scrn = Screen(name='Add_Configs')
        add_configs = Add_Configs(self.sm)
        scrn.add_widget(add_configs)
        scrn.bind(on_enter=add_configs.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Configs')
        delete_configs = Delete_Configs(self.sm)
        scrn.add_widget(delete_configs)
        scrn.bind(on_enter=delete_configs.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Configs')
        scrn.add_widget(Settings_Configs(self.sm))
        self.sm.add_widget(scrn)
        # Customers
        scrn = Screen(name='Add_Customers')
        add_customers = Add_Customers(self.sm)
        scrn.add_widget(add_customers)
        scrn.bind(on_enter=add_customers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Customers')
        delete_customers = Delete_Customers(self.sm)
        scrn.add_widget(delete_customers)
        scrn.bind(on_enter=delete_customers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Edit_Customers')
        edit_customers = Edit_Customers(self.sm)
        scrn.add_widget(edit_customers)
        scrn.bind(on_enter=edit_customers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Customers')
        scrn.add_widget(Settings_Customers(self.sm))
        self.sm.add_widget(scrn)
        # Patterns
        scrn = Screen(name='Add_Patterns')
        add_patterns = Add_Patterns(self.sm)
        scrn.add_widget(add_patterns)
        scrn.bind(on_enter=add_patterns.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Patterns')
        delete_patterns = Delete_Patterns(self.sm)
        scrn.add_widget(delete_patterns)
        scrn.bind(on_enter=delete_patterns.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Edit_Patterns')
        edit_patterns = Edit_Patterns(self.sm)
        scrn.add_widget(edit_patterns)
        scrn.bind(on_enter=edit_patterns.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Patterns')
        scrn.add_widget(Settings_Patterns(self.sm))
        self.sm.add_widget(scrn)
        # Vehicles
        scrn = Screen(name='Add_Vehicles')
        add_vehicles = Add_Vehicles(self.sm)
        scrn.add_widget(add_vehicles)
        scrn.bind(on_enter=add_vehicles.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Vehicles')
        delete_vehicles = Delete_Vehicles(self.sm)
        scrn.add_widget(delete_vehicles)
        scrn.bind(on_enter=delete_vehicles.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Edit_Vehicles')
        edit_vehicles = Edit_Vehicles(self.sm)
        scrn.add_widget(edit_vehicles)
        scrn.bind(on_enter=edit_vehicles.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Vehicles')
        scrn.add_widget(Settings_Vehicles(self.sm))
        self.sm.add_widget(scrn)
        # Workers
        scrn = Screen(name='Add_Workers')
        add_workers = Add_Workers(self.sm)
        scrn.add_widget(add_workers)
        scrn.bind(on_enter=add_workers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Workers')
        delete_workers = Delete_Workers(self.sm)
        scrn.add_widget(delete_workers)
        scrn.bind(on_enter = delete_workers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Edit_Workers')
        edit_workers = Edit_Workers(self.sm)
        scrn.add_widget(edit_workers)
        scrn.bind(on_enter=edit_workers.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Workers')
        scrn.add_widget(Settings_Workers(self.sm))
        self.sm.add_widget(scrn)
        # Stillage_types
        scrn = Screen(name='Add_Stillage_types')
        add_stillage_types = Add_Stillage_type(self.sm)
        scrn.add_widget(add_stillage_types)
        scrn.bind(on_enter=add_stillage_types.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Delete_Stillage_types')
        delete_stillage_types = Delete_Stillage_type(self.sm)
        scrn.add_widget(delete_stillage_types)
        scrn.bind(on_enter=delete_stillage_types.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Edit_Stillage_types')
        edit_stillage_types = Edit_Stillage_type(self.sm)
        scrn.add_widget(edit_stillage_types)
        scrn.bind(on_enter=edit_stillage_types.clear_screen)
        self.sm.add_widget(scrn)

        scrn = Screen(name='Settings_Stillage_types')
        scrn.add_widget(Settings_Stillage_types(self.sm))
        self.sm.add_widget(scrn)
        # Exports settings
        scrn = Screen(name='Settings_Exports')
        settings_exports = Settings_Exports(self.sm)
        scrn.add_widget(settings_exports)
        scrn.bind(on_enter=settings_exports.clear_screen)
        self.sm.add_widget(scrn)

        ###########
        self.zamestnanec = None
        self.kod = []

        self.skenovanieScreen = Scanner2(self.screenManager, self.kod, None, None,
                                        name='skener')
        self.screenManager.add_widget(self.skenovanieScreen)
        self.skenovanieScreen.prveSpustenie = False

        self.startScreen = StartScreen('uvod', 'Menu_screen', self, name='startScreen')
        self.screenManager.add_widget(self.startScreen)

        # Menu screen
        scrn = Screen(name='Menu_screen')
        ms = Menu_screen(self, self.startScreen, 'uvodAudit')
        scrn.add_widget(ms)
        scrn.bind(on_enter=ms.vytvorMenu)
        self.sm.add_widget(scrn)

        self.auditUvodScreen = UvodAuditu(self, self.startScreen, self.startScreen, name='uvodAudit')
        self.screenManager.add_widget(self.auditUvodScreen)

        self.prebiehajuciAudit = PrebiehajuciAudit(self, self.auditUvodScreen, None, None,
                                                   name='priebehAuditu')
        self.screenManager.add_widget(self.prebiehajuciAudit)

        self.uzavretyScreen = UzavretyKamion(self, self.prebiehajuciAudit, self.auditUvodScreen, name='uzavrety')
        self.screenManager.add_widget(self.uzavretyScreen)


        self.auditov = 0
        self.audit = None
        self.shippment = None
        self.shippmentStillages = set()
        self.vozikyVOprave = {}
        self.sm.current = 'startScreen'
        #self.sm.current = 'Menu_screen'
        return self.sm
if __name__ == '__main__':
    from sqlite import User, User_Role
    print("zamstnanci")
    for u in User().vrat_vsetky():
        print(u, User_Role().stiahni(u['User_Role_id']).name)
    MainApp().run()
