#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import General
class Settings_Exports (BoxLayout):
    """
    nastavenia Exportov
    """
    selected_answer = None
    notify = Button(text = '')
    drop1 = DropDown()
    btn1 = Button(text="Nastav")
    btn2 = Button(text="Späť")
    screenManager = None
    values=[]
    def __init__(self, screenManager,**kwargs):
        super(Settings_Exports, self).__init__(**kwargs)
        self.screenManager = screenManager
    def set_selected(self,text):
        """
        nastavi vybratu moznost
        """
        self.selected_answer = 0
        if text == "Áno":
            self.selected_answer = 1
    def call_Back (self):
        """
        vrati naspat na povodnu obrazovku
        """
        self.screenManager.current = 'Menu_screen'
    def check (self):
        """
        updatuje databazu
        """
        if self.selected_answer is None:
            self.notify.text = "Please select one of opportunities"
        else:
            on_update_exporting = General().stiahni(General().vrat_vsetky()[-1]['id'])
            on_update_exporting.Automatic_export = self.selected_answer
            on_update_exporting.update()
            self.call_Back()
    def clear_screen(self,*args):
        """
        nacitanie obrazovky
        """
        self.notify.text = ""
        # self.drop1.clear_widgets()
        self.values = []
        id = General().vrat_vsetky()[-1]['Automatic_export']
        for i in ["Áno","Nie"]:
            self.values.append(i)
        self.ids.spinner_export.values = self.values
        self.selected_answer = None
        if id == 0:
            self.ids.spinner_export.text = "Nie"
            self.selected_answer = 1
        if id == 1:
            self.ids.spinner_export.text= "Áno"
            self.selected_answer = 0