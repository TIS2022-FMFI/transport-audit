from kivy.lang import Builder

from Menu_screen import *
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from startScreen2 import StartScreen
from UzavretyAudit import UzavretyKamion
from priebehAuditu import PrebiehajuciAudit
from kivy.core.window import Window

from auditUvod import UvodAuditu
from kivy.utils import platform
if platform == "android": # Zarucuje, že iba na androide sa if spustí, teda android package sa nemusí (a ani nedá) inštalovať
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,Permission.CAMERA, Permission.INTERNET])

from sqlite import synchronize_db_server_client
from logy import logy_nahraj_vsetky_na_server,logni


from kivy.clock import Clock
try:
    synchronize_db_server_client()
    logy_nahraj_vsetky_na_server()
except:
    print("neda sa pripojit")
    logni(0,202,"chyba pri synchroniizácii")
from skener2 import Scanner as Scanner2
from parser import ziskaj_report, citaj_report_dict


class MainApp(App):
    spatZoScreenov = {}
    report = {}
    zamestnanec = None
    def kontrolaSpat(self, window, key, *args):
        if key == 27:
            screen = self.sm.current
            funkcia = self.spatZoScreenov.get(screen)
            if funkcia is not None:
                funkcia()

            return True
        return False

    def stiahnutieReportu(self, *args):
        kod = 0

        if self.zamestnanec is not None:
            kod = self.zamestnanec.code
        print(kod, "stahuje report")
        ziskaj_report(kod)

    def udajeReportu(self, kod):
        try:
            self.report = citaj_report_dict()
        except:
            logni(kod, 205, "nepodarilo sa precitat report")
        return self.report
    def build(self):
        if platform == "android":
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA, Permission.INTERNET])
        Builder.load_file('design.kv')

        Window.bind(on_keyboard=self.kontrolaSpat)
        self.stiahnutieReportu()
        Clock.schedule_interval(self.stiahnutieReportu, 15 * 60)
        #Vehicle().stiahni('9a414a42-1edc-42dc-a562-e635de6db7d2').zmazat()
        self.sm = self.screenManager = ScreenManager()
        # Configs
        scrn = Screen(name='Add_Configs')
        add_configs = Add_Configs(self.sm)
        scrn.add_widget(add_configs)
        scrn.bind(on_enter=add_configs.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Configs'] = add_configs.call_Back

        scrn = Screen(name='Delete_Configs')
        delete_configs = Delete_Configs(self.sm)
        scrn.add_widget(delete_configs)
        scrn.bind(on_enter=delete_configs.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Configs'] = delete_configs.call_Back

        scrn = Screen(name='Settings_Configs')
        setConf = Settings_Configs(self.sm)
        scrn.add_widget(setConf)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Configs'] = setConf.call_back
        # Customers
        scrn = Screen(name='Add_Customers')
        add_customers = Add_Customers(self.sm)
        scrn.add_widget(add_customers)
        scrn.bind(on_enter=add_customers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Customers'] = add_customers.call_Back

        scrn = Screen(name='Delete_Customers')
        delete_customers = Delete_Customers(self.sm)
        scrn.add_widget(delete_customers)
        scrn.bind(on_enter=delete_customers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Customers'] = delete_customers.call_Back

        scrn = Screen(name='Edit_Customers')
        edit_customers = Edit_Customers(self.sm)
        scrn.add_widget(edit_customers)
        scrn.bind(on_enter=edit_customers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Edit_Customers'] = edit_customers.call_Back

        scrn = Screen(name='Settings_Customers')
        setCust = Settings_Customers(self.sm)
        scrn.add_widget(setCust)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Customers'] = setCust.call_back
        # Patterns
        scrn = Screen(name='Add_Patterns')
        add_patterns = Add_Patterns(self.sm)
        scrn.add_widget(add_patterns)
        scrn.bind(on_enter=add_patterns.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Patterns'] = add_patterns.call_Back

        scrn = Screen(name='Delete_Patterns')
        delete_patterns = Delete_Patterns(self.sm)
        scrn.add_widget(delete_patterns)
        scrn.bind(on_enter=delete_patterns.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Patterns'] = delete_patterns.call_Back

        scrn = Screen(name='Edit_Patterns')
        edit_patterns = Edit_Patterns(self.sm)
        scrn.add_widget(edit_patterns)
        scrn.bind(on_enter=edit_patterns.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Edit_Patterns'] = edit_patterns.call_Back

        scrn = Screen(name='Settings_Patterns')
        setPatt = Settings_Patterns(self.sm)
        scrn.add_widget(setPatt)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Patterns'] = setPatt.call_back
        # Vehicles
        scrn = Screen(name='Add_Vehicles')
        add_vehicles = Add_Vehicles(self.sm)
        scrn.add_widget(add_vehicles)
        scrn.bind(on_enter=add_vehicles.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Vehicles'] = add_vehicles.call_Back

        scrn = Screen(name='Delete_Vehicles')
        delete_vehicles = Delete_Vehicles(self.sm)
        scrn.add_widget(delete_vehicles)
        scrn.bind(on_enter=delete_vehicles.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Vehicles'] = delete_vehicles.call_Back

        scrn = Screen(name='Edit_Vehicles')
        edit_vehicles = Edit_Vehicles(self.sm)
        scrn.add_widget(edit_vehicles)
        scrn.bind(on_enter=edit_vehicles.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Edit_Vehicles'] = edit_vehicles.call_Back

        scrn = Screen(name='Settings_Vehicles')
        setVehi = Settings_Vehicles(self.sm)
        scrn.add_widget(setVehi)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Vehicles'] = setVehi.call_back

        # Workers
        scrn = Screen(name='Add_Workers')
        add_workers = Add_Workers(self.sm)
        scrn.add_widget(add_workers)
        scrn.bind(on_enter=add_workers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Workers'] = add_workers.call_Back

        scrn = Screen(name='Delete_Workers')
        delete_workers = Delete_Workers(self.sm)
        scrn.add_widget(delete_workers)
        scrn.bind(on_enter = delete_workers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Workers'] = delete_workers.call_Back

        scrn = Screen(name='Edit_Workers')
        edit_workers = Edit_Workers(self.sm)
        scrn.add_widget(edit_workers)
        scrn.bind(on_enter=edit_workers.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Edit_Workers'] = edit_workers.call_Back

        scrn = Screen(name='Settings_Workers')
        setWork = Settings_Workers(self.sm)
        scrn.add_widget(setWork)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Workers'] = setWork.call_back

        # Stillage_types
        scrn = Screen(name='Add_Stillage_types')
        add_stillage_types = Add_Stillage_type(self.sm)
        scrn.add_widget(add_stillage_types)
        scrn.bind(on_enter=add_stillage_types.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Add_Stillage_types'] = add_stillage_types.call_Back

        scrn = Screen(name='Delete_Stillage_types')
        delete_stillage_types = Delete_Stillage_type(self.sm)
        scrn.add_widget(delete_stillage_types)
        scrn.bind(on_enter=delete_stillage_types.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Delete_Stillage_types'] = delete_stillage_types.call_Back

        scrn = Screen(name='Edit_Stillage_types')
        edit_stillage_types = Edit_Stillage_type(self.sm)
        scrn.add_widget(edit_stillage_types)
        scrn.bind(on_enter=edit_stillage_types.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Edit_Stillage_types'] = edit_stillage_types.call_Back

        scrn = Screen(name='Settings_Stillage_types')
        setStil = Settings_Stillage_types(self.sm)
        scrn.add_widget(setStil)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Stillage_types'] = setStil.call_back

        # Exports settings
        scrn = Screen(name='Settings_Exports')
        settings_exports = Settings_Exports(self.sm)
        scrn.add_widget(settings_exports)
        scrn.bind(on_enter=settings_exports.clear_screen)
        self.sm.add_widget(scrn)
        self.spatZoScreenov['Settings_Exports'] = settings_exports.call_Back

        ###########

        self.kod = []

        #skener
        self.skenovanieScreen = Scanner2(self.screenManager, self.kod, None, None,
                                        name='skener')
        self.screenManager.add_widget(self.skenovanieScreen)
        self.skenovanieScreen.prveSpustenie = False
        self.spatZoScreenov['skener'] = self.skenovanieScreen.spat

        #start screen
        self.startScreen = StartScreen('uvod', 'Menu_screen', self, name='startScreen')
        self.screenManager.add_widget(self.startScreen)

        # Menu screen
        self.scrnMenu = Screen(name='Menu_screen')
        ms = Menu_screen(self, self.startScreen, 'uvodAudit')
        self.scrnMenu.add_widget(ms)
        self.scrnMenu.bind(on_enter=ms.vytvorMenu)
        self.sm.add_widget(self.scrnMenu)

        #uvod auditu
        self.auditUvodScreen = UvodAuditu(self, self.scrnMenu, self.startScreen, name='uvodAudit')
        self.screenManager.add_widget(self.auditUvodScreen)
        self.spatZoScreenov['uvodAudit'] = self.auditUvodScreen.spat

        #priebeh auditu
        self.prebiehajuciAudit = PrebiehajuciAudit(self, self.auditUvodScreen, None, None,
                                                   name='priebehAuditu')
        self.screenManager.add_widget(self.prebiehajuciAudit)

        #uzavrety kamion
        self.uzavretyScreen = UzavretyKamion(self, self.prebiehajuciAudit, self.auditUvodScreen, name='uzavrety')
        self.screenManager.add_widget(self.uzavretyScreen)
        self.spatZoScreenov['uzavrety'] = self.uzavretyScreen.otvorit


        self.auditov = 0
        self.audit = None
        self.shippment = None
        self.shippmentStillages = set()
        self.vozikyVOprave = {}

        self.sm.current = 'startScreen'
        # self.sm.current = 'Menu_screen'
        return self.sm
if __name__ == '__main__':
    from sqlite import User, User_Role
    MainApp().run()
