#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import User, User_Role
class Add_Workers (BoxLayout):
    selected_role = None
    notify = Button(text = '')
    drop1 = DropDown()
    text1 = TextInput(text='Meno')
    text2 = TextInput(text='Priezvisko')
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Späť")
    screenManager = None
    values=[]
    # #2F3C7E
    def __init__(self, screenManager,**kwargs):
        super(Add_Workers, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.drop1 = self.ids.spinner_id
        self.text1 = self.ids.input
        self.text2 = self.ids.input1
        self.notify = self.ids.notify
    def synchronize_user_roles(self):
        self.selected_role = None
        for i in User_Role().vrat_vsetky():
            self.values.append(i["name"])

        self.ids.spinner_id.values = self.values
        self.ids.spinner_id.text = 'Vyber rolu'

    def set_selected(self,text):
        if self.values.count(text) == 0:
            return
        self.selected_role = text
    def call_Back (self):
        self.screenManager.current = 'Settings_Workers'
    def check (self):
        print(self.selected_role)
        if  len([x for x in self.text1.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) != len(self.text1.text) or self.text1.text == "Meno":
            self.notify.text = "Please enter a valid first name."
        elif  len([x for x in self.text2.text if ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) > ord('A') and ord(x) < ord('Z')))]) != len(self.text2.text) or self.text2.text == "Priezvisko":
            self.notify.text = "Please enter a valid last name."
        elif self.text1.text == "" or self.text2.text == "":
            self.notify.text = "Please choose names fields"
        elif self.selected_role is None:
            self.notify.text = "Please choose user_role"
        else:
            for i in (User_Role().vrat_vsetky()):
                if self.selected_role == i["name"]:
                    self.selected_role = i["id"]
                    break
            User().nahraj(self.text1.text, self.text2.text, self.selected_role)
            self.call_Back()
    def clear_screen(self,*args):
        self.text1.text = ""
        self.text2.text = ""
        self.notify.text = ""
        self.synchronize_user_roles()

