#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.screenmanager import Screen
from sqlite import User
class Delete_Workers (BoxLayout):
    """
    mazanie zamestnancov
    """
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaž")
    btn2 = Button(text="Späť")
    btn3 = Button(text = "Užívateľský kód")
    screenManager = None
    workers_list = None
    values=[]
    def __init__(self, screenManager, **kwargs):
        super(Delete_Workers, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.notify = self.ids.notify
        self.btn3 = self.ids.button_delete_worker
    def synchronize_workers(self,*args):
        """
        nacita zamestnancov z databazy
        """
        self.on_delete_selected = None
        self.values = []
        self.workers_list = dict([(i['Name'][0] + ". " + i['Last_name'] + " " + str(i['code']), str(i['code'])) for i in User().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.ids.spinner_delete_worker.values = []
        for i in self.workers_list:
            self.values.append(i)
        self.ids.spinner_delete_worker.values = self.values
        self.ids.spinner_delete_worker.text = 'Vyber pracovníka na vymazanie'

    def select_code(self,text):
        """
        oznaci zamestnanca na vymazanie
        """
        if text not in self.workers_list:
            return
        tex = self.workers_list[text]
        self.btn3.text = tex
        self.on_delete_selected = tex
    def call_Back (self):
        """
        presunutie sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Workers'
    def check (self):
        """
        kontrola vstupov nasledne mazanie zamestnanca
        """
        if (self.on_delete_selected is None):
                self.notify.text = "Prosím vyberte zamestnanca."
        else:
            on_delete_user = User().stiahni(int(self.on_delete_selected))
            on_delete_user.zmazat()
            self.call_Back()

    def clear_screen(self, *args):
        """
        prvotna inicializacia obrazovky
        """
        self.notify.text = ""
        self.btn3.text = "Užívateľský kód"
        self.synchronize_workers()