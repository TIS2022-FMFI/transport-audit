from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Stillage_type
class Edit_Stillage_type (BoxLayout):
    select_id  = None
    notify = Button(text = '')
    text1 = TextInput(text='Meno typu vozika')
    drop1 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    stillage_type_list = None
    screenManager = None
    values = []
    def synchronize_stillage_types(self):
        self.select_id = None
        self.values = []
        self.stillage_type_list = dict([(i['Name'], i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.stillage_type_list:
            self.values.append(i)
        self.ids.spinner_edit_st.values = self.values
        self.ids.spinner_edit_st.text = "Vyber stillage type na upravu"
    def __init__(self,screenManager, **kwargs):
        super(Edit_Stillage_type, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_edit_st
        self.notify = self.ids.notify
    def set_widgets(self,tex1):
        if tex1 not in self.stillage_type_list:
            return
        self.text1.text = tex1
        self.select_id = self.stillage_type_list[tex1]
    def call_Back (self):
        self.screenManager.current = 'Settings_Stillage_types'
    def check (self):
        if (self.select_id is None):
                self.notify.text = "Please choose stillage type you want edit."
        elif self.text1.text in self.stillage_type_list.keys() and self.stillage_type_list[self.text1.text] != self.select_id:
            self.notify.text = "This stillage_type already exists"
        elif self.text1.text == "" or self.text1.text == "Vyber stillage type na upravu":
            self.notify.text = "Please enter a valid first name."
        else:
            updated_stillage_type = Stillage_type().stiahni(self.select_id)
            updated_stillage_type.Name = self.text1.text
            updated_stillage_type.update()
            self.call_Back()
    def clear_screen(self, *args):
        self.text1.text = ""
        self.notify.text = ""
        self.synchronize_stillage_types()