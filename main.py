from scanner import *
from kivy.uix.dropdown import  DropDown
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.core.window import Window
class GefcoApp(App):
    def build(self):
        camlayout = FloatLayout(size=(600, 600))
        Window.clearcolor = (0,0,1,1)
        dropdown = DropDown()
        for i in ["Slovak","English"]:
            btn = Button(text=i,background_color = (138/255,43/255,226/255,1), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        choose_language = Button(text = 'Choose language', background_color = (138/255,43/255,226/255,1),size_hint = (.2,None), pos = (350,70))
        choose_language.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(choose_language, 'text', x))
        camlayout.add_widget(choose_language)
        runTouchApp(camlayout)

        # choose_language

if __name__ == '__main__':
    # CamApp().run()
    GefcoApp().run()
