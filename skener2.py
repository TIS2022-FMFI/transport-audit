from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy_garden.zbarcam import ZBarCam
from kivy.uix.textinput import TextInput


class Scanner(Screen):
    def __init__(self, screenManager, kody, povodnaScreen, dalsiaScreen, **kwargs):
        super(Scanner, self).__init__(**kwargs)

        self.prveSpustenie = True
        self.i = 0
        self.screenManager = screenManager
        self.kody = kody
        self.najdene = None
        self.povodnaScreen = povodnaScreen
        self.dalsiaScreen = dalsiaScreen
        self.orientation = 'vertical'  # vertical placing of widgets

        # self.zbarcam = ZBarCam(size_hint_y = 0.6, size_hint_x = 1, pos_hint = {'center_y': 0.65})
        self.zbarcam = self.ids.img
        self.zbarcam.stop()

        self.skenovat = False
        self.bind(on_enter=self.zapnutieKamery)

        self.butNove = self.ids.btnNove
        self.butPouzit = self.ids.btnPouzit
        self.butNove.disabled = True
        self.butPouzit.disabled = True

        self.zadanyKod = self.ids.input

        Clock.schedule_interval(self.read_text, 1)

    def zapnutieKamery(self, *args):
        """
            spusti kameru a umozni detekciu kodov
        """
        if self.prveSpustenie:
            self.prveSpustenie = False
            self.skenovat = False
            return

        self.zadanyKod.text = ''
        self.skenovat = True
        self.zbarcam.start()

    def pokracovat(self, *args):
        """
            po zdetekovani kodu umozni naskenovat dalsi kod
        """
        self.skenovat = True
        self.precButtonyKody()

    def precButtonyKody(self):
        """
            ak je prave zobrazovany naskenovany kod, znefunkcnime buttony skenovaneho kodu a na pokracovanie skenovania
        """
        if self.butNove is None:
            return
        self.butNove.disabled = True
        self.butPouzit.disabled = True

    def pouzitZadany(self, *args):
        """
            ak kod v poli na zadavanie neprazdny, tak ho vlozi do pola a zavola spat
        """
        kod = self.zadanyKod.text.strip()
        if kod:
            self.kody.clear()
            self.kody.append(kod)
        self.spat()

    def spat(self, *args):
        """
            zastavi a odpoji kameru, zrusi detekciu kodov, odstrani pripadne buttony na vyber kodu
            nasledne sa prepne na predchadzajucu screen
        """
        self.zbarcam.stop()
        self.remove_widget(self.zbarcam)
        self.skenovat = False
        self.precButtonyKody()

        self.screenManager.current = self.povodnaScreen

    def koniec(self, *args):
        """
            ulozi naskenovany kod do pola, a zavola metodu spat
        """
        self.kody.clear()
        self.kody.append(self.najdene)
        self.spat()

    def pouzitKod(self, kod):
        """
            ulozi si naskenovany kod, vypne detekciu kodov a spristupni buttony na vyber kodu a pokracovanie v skenovani
            :param kod: naskenovany kod ktory si chceme ulozit
        """
        self.skenovat = False
        self.najdene = kod
        self.butNove.disabled = False
        self.butPouzit.disabled = False
        self.butNove.text = f'skenovať ďalej'
        self.butPouzit.text = f'{kod}'



    def read_text(self, *args):
        """
            ak je prave skenovanie, a kamera detekuje aspon jeden kod, zavola metodu pouziKod s prvym detekovanym kodom
        """
        if self.zbarcam is None or not self.skenovat:
            return

        if self.zbarcam.symbols:
            self.pouzitKod(str(self.zbarcam.symbols[0].data, 'UTF-8'))
