from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Stillage_type
class Delete_Stillage_type (BoxLayout):
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    stillage_type_list = None
    screenManager = None
    values = []
    def synchronize_stillage_types(self):
        self.on_delete_selected = None
        self.stillage_type_list = dict([(i['Name'],i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.values = []
        for i in self.stillage_type_list:
            self.values.append(i)
        self.ids.spinner_delete_st.values = self.values
        self.ids.spinner_delete_st.text = "Vyber stillage type na vymazanie"
    def __init__(self, screenManager,**kwargs):
        super(Delete_Stillage_type, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
    def select_code(self,tex):
        if tex not in self.stillage_type_list:
            return
        self.on_delete_selected = self.stillage_type_list[tex]
    def call_Back (self):
        self.screenManager.current = 'Settings_Stillage_types'
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Please choose Stillage type by name you want delete."
        else:
            on_delete_stillage_type = Stillage_type().stiahni(self.on_delete_selected)
            on_delete_stillage_type.zmazat()
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.synchronize_stillage_types()