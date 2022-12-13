from Menu_screen import *
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
class MainApp(App):
    def build(self):
        self.sm = ScreenManager()
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

        scrn = Screen(name='Edit_Configs')
        edit_configs = Edit_Configs(self.sm)
        scrn.add_widget(edit_configs)
        scrn.bind(on_enter=edit_configs.clear_screen)
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
        #Menu screen
        scrn = Screen (name = 'Menu_screen')
        scrn.add_widget(Menu_screen(self.sm))
        self.sm.add_widget(scrn)
        self.sm.current = 'Menu_screen'
        return self.sm
if __name__ == '__main__':
    MainApp().run()
