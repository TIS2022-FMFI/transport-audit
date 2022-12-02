from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import User
class Delete_Workers (BoxLayout):
    notify = Button(text = '')
    on_delete_selected = None
    drop1 = DropDown()
    btn1 = Button(text="Vymaz")
    btn2 = Button(text="Späť")
    def __init__(self, **kwargs):
        super(Delete_Workers, self).__init__(**kwargs)        
        for i in User().vrat_vsetky():
            btn = Button(text= str(i['code']), size_hint_y=None, height=40, on_release=lambda btn: self.select_code(btn.text))
            btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
            self.drop1.add_widget(btn)
        mainbutton1 = Button(text='Vyber pracovnika na vymazanie', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.add_widget(mainbutton1)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def select_code(self,tex):
        self.on_delete_selected  = tex
    def call_Back (self):
        App.get_running_app().stop()        
    def check (self):
        if (self.on_delete_selected is None):
                self.notify.text = "Please choose user by code you want delete."
        else:
            on_delete_user = User().stiahni(int(self.on_delete_selected))
            on_delete_user.Name = None
            on_delete_user.update()
            self.call_Back()
class Deleting (App):
    def build(self):return Delete_Workers()
