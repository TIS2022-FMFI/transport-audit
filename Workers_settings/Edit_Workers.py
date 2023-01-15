#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import User, User_Role
class Edit_Workers (BoxLayout):
    select_role = None
    select_code  = None
    notify = Button(text = '')
    text1 = TextInput(text='Meno')
    text2 = TextInput(text='Priezvisko')
    drop1 = DropDown()
    drop2 = DropDown()
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    btn3 = Button(text="Uzivatelsky kod")
    workers_list = None
    screenManager = None
    values1=[]
    values2=[]
    def __init__(self, screenManager,**kwargs):
        super(Edit_Workers, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.text1 = self.ids.input_edit_worker_1
        self.text2 = self.ids.input_edit_worker_2
        self.btn3 = self.ids.button_edit_worker
        self.notify = self.ids.notify
    def synchronize_workers(self):
        self.select_code = None
        self.workers_list = dict([(i['Name'][0] + ". " + i['Last_name'] + " " + str(i['code']), str(i['code'])) for i in User().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.workers_list:
            self.values2.append(i)
        self.ids.spinner_edit_worker_1.values = self.values2
        self.ids.spinner_edit_worker_1.text = 'Vyber pracovnika na upravu'
    def synchronize_user_roles(self):
        self.select_code = None
        for i in User_Role().vrat_vsetky():
            self.values1.append(i["name"])
        self.ids.spinner_edit_worker_2.values = self.values1
        self.ids.spinner_edit_worker_2.text = 'Vyber rolu'
    def set_select(self,tex):
        self.select_role = tex
    def set_widgets(self,text):
        if text not in self.workers_list:
            return
        tex1 = self.workers_list[text]
        select_user = User().stiahni(int(tex1))
        self.text1.text = select_user.Name
        print(select_user.Name)
        self.text2.text = select_user.Last_name
        selected_role = User_Role().stiahni(select_user.User_Role_id)
        self.select_code = tex1
        self.btn3.text = tex1
        if (selected_role is not None):

            self.drop1.select(selected_role.name)
            self.select_role = selected_role.name
            self.ids.spinner_edit_worker_2.text = self.select_role
    def call_Back (self):
        self.screenManager.current = 'Settings_Workers'
    def check (self):
        if (self.select_code is None):
                self.notify.text = "Please choose user by code you want edit."
        elif len([x for x in self.text1.text if
                ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) >= ord('A') and ord(x) <= ord('Z')))]) != len(
                self.text1.text) or self.text1.text == "Meno":
            self.notify.text = "Please enter a valid first name."
        elif len([x for x in self.text2.text if
                  ((ord(x) >= ord('a') and ord(x) <= ord('z')) or (ord(x) > ord('A') and ord(x) < ord('Z')))]) != len(
                self.text2.text) or self.text2.text == "Priezvisko":
            self.notify.text = "Please enter a valid last name."
        elif self.text1.text == "" or self.text2.text == "":
            self.notify.text = "Please choose names fields"
        elif self.select_role is None:
            self.notify.text = "Please choose user_role"
        else:
            updated_user = User().stiahni(self.select_code)
            updated_user.Name = self.text1.text
            updated_user.Last_name = self.text2.text
            for i in (User_Role().vrat_vsetky()):
                if self.select_role == i["name"]:
                    updated_user.User_Role_id = i["id"]
                    break
            updated_user.update()
            self.call_Back()
    def clear_screen(self,*args):
        self.text1.text = ""
        self.text2.text = ""
        self.notify.text = ""
        self.btn3.text="Uzivatelsky kod"
        self.synchronize_user_roles()
        self.synchronize_workers()