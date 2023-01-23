from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Stillage_type
class Edit_Stillage_type (BoxLayout):
    """
    uprava typov vozika
    """
    select_id  = None
    notify = Button(text = '')
    text1 = TextInput(text='Meno typu vozíka')
    drop1 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    stillage_type_list = None
    screenManager = None
    values = []
    def synchronize_stillage_types(self):
        """
        natiahne typy vozikov z databazy
        """
        self.select_id = None
        self.values = []
        self.stillage_type_list = dict([(i['Name'], i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.stillage_type_list:
            self.values.append(i)
        self.ids.spinner_edit_st.values = self.values
        self.ids.spinner_edit_st.text = "Vyber typ vozíka na úpravu"
    def __init__(self,screenManager, **kwargs):
        super(Edit_Stillage_type, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_edit_st
        self.notify = self.ids.notify
    def set_widgets(self,tex1):
        """
        ulozi vybraty typ vozika a nacita do textoveho pola jeho meno ktore vieme upravit
        """
        if tex1 not in self.stillage_type_list:
            return
        self.text1.text = tex1
        self.select_id = self.stillage_type_list[tex1]
    def call_Back (self):
        """
        vrati sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Stillage_types'
    def check (self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne updatne typ vozika v databze
        """
        if (self.select_id is None):
                self.notify.text = "Vyber typ vozíka"
        elif self.text1.text in self.stillage_type_list.keys() and self.stillage_type_list[self.text1.text] != self.select_id:
            self.notify.text = "Typ vozíka už existuje"
        elif self.text1.text == "" or self.text1.text == "Vyber typ vozíka na úpravu":
            self.notify.text = "Zadaj názov"
        else:
            updated_stillage_type = Stillage_type().stiahni(self.select_id)
            updated_stillage_type.Name = self.text1.text
            updated_stillage_type.update()
            self.call_Back()
    def clear_screen(self, *args):
        """
        nacitanie udajov
        """
        self.text1.text = ""
        self.notify.text = ""
        self.synchronize_stillage_types()