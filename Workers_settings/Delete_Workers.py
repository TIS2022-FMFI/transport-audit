#from scanner import *
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.screenmanager import Screen
from sqlite import User
class Delete_Workers (BoxLayout):
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    btn3 = Button(text = "Uzivatelsky kod")
    screenManager = None
    workers_list = None
    def __init__(self, screenManager, **kwargs):
        super(Delete_Workers, self).__init__(**kwargs)
        self.screenManager = screenManager
        # self.bind(on_enter = self.fill_worker_list)
        mainbutton1 = Button(text='Vyber pracovnika na vymazanie', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(self.btn3)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def synchronize_workers(self,*args):
        self.on_delete_selected = None
        self.workers_list = dict([(i['Name'][0] + ". " + i['Last_name'] + " " + str(i['code']), str(i['code'])) for i in User().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.drop1.clear_widgets()
        self.drop1.select('Vyber pracovnika na vymazanie')
        for i in self.workers_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.select_code(self.workers_list[btn.text]))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
    def select_code(self,tex):
        self.btn3.text = tex
        self.on_delete_selected  = tex
    def call_Back (self):
        self.screenManager.current = 'Settings_Workers'
        # self.screenManager.get_screen('Delete_Workers').clear_widgets()
        # self.screenManager.get_screen('Delete_Workers').add_widget(super(Delete_Workers, self))
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Please choose user by code you want delete."
        else:
            on_delete_user = User().stiahni(int(self.on_delete_selected))
            on_delete_user.zmazat()
            self.call_Back()

    def clear_screen(self, *args):
        self.notify.text = ""
        self.btn3.text = "Uzivatelsky kod"
        self.synchronize_workers()