#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import General
class Settings_Exports (BoxLayout):
    selected_answer = None
    notify = Button(text = '')
    drop1 = DropDown()
    btn1 = Button(text="Nastav")
    btn2 = Button(text="Späť")
    screenManager = None
    def __init__(self, screenManager,**kwargs):
        super(Settings_Exports, self).__init__(**kwargs)
        self.screenManager = screenManager
        mainbutton = Button(text='Vyber autoexport', size_hint=(.5, .25),pos=(60, 20))
        mainbutton.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def set_selected(self,text):
        self.selected_answer = text
    def call_Back (self):
        self.screenManager.current = 'Menu_screen'
    def check (self):
        if self.selected_answer is None:
            self.notify.text = "Please select one of opportunities"
        else:
            self.call_Back()
    def clear_screen(self,*args):
        self.notify.text = ""
        self.selected_answer = None
        self.drop1.clear_widgets()
        self.drop1.select('Vyber autoexport')
        for i in ["Yes","No"]:
            btn = Button(text=i, size_hint_y=None, height=40,on_release=lambda btn: self.set_selected(btn.text))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
