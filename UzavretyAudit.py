from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class UzavretyKamion(Screen):
    def __init__(self, aplikacia, povodna, dalsia, **kwargs):
        super().__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.dalsia = dalsia

        logo = Image(source='logo.webp')
        logo.size_hint_x = 0.2
        logo.pos_hint = {'center_x': 0.5, 'top': 1.3}
        self.add_widget(logo)

        self.lUzavrete = Label(text='Vozidlo je uzavrete', pos_hint={'center_x': 0.5, "top": 0.5}, size_hint=(0.6, 0.12), font_size='40sp')
        self.add_widget(self.lUzavrete)

        bOtvorit = Button(text='Otvorit vozidlo', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.5, "top": 0.2}, size_hint=(1, 0.08))
        bOtvorit.bind(on_press=self.otvorit)
        self.add_widget(bOtvorit)

        bNovyAudit = Button(text='Dalsi audit', background_color="#0003a8",
                          background_normal="", pos_hint={'center_x': 0.5, "top": 0.1}, size_hint=(1, 0.08))
        bNovyAudit.bind(on_press=self.novyAudit)
        self.add_widget(bNovyAudit)


    def otvorit(self, *args):
        self.aplikacia.screenManager.current = self.povodna.name

    def novyAudit(self, *args):
        self.povodna.spat()