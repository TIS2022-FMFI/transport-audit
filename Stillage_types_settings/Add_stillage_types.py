from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Stillage_type
class Add_Stillage_type (BoxLayout):
    notify = Button(text = '')
    text1 = TextInput()
    screenManager = None
    stillage_type_list = None
    def __init__(self,screenManager, **kwargs):
        super(Add_Stillage_type, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_add_st
        self.notify = self.ids.notify
    def synchronize_stillage_types(self):
        self.stillage_type_list = [i['Name'] for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED']
    def call_Back (self):
        # dorob
        self.screenManager.current = 'Settings_Stillage_types'
    def check (self):
        if  self.text1.text=="" or self.text1.text == 'Meno typu vozika':
            self.notify.text = "Please enter a valid name."
        elif self.text1.text in self.stillage_type_list:
            self.notify.text = "Name already exists"
        else:
            Stillage_type().nahraj(self.text1.text)
            self.call_Back()
    def clear_screen(self, *args):
        self.notify.text = ""
        self.text1.text = ''
        self.synchronize_stillage_types()