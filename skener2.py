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

        # self.butSpat = Button(text='Späť', size_hint_y=None, height='48dp', on_press=self.spat,
        #                       pos_hint={'center_y': 0.05})
        # self.add_widget(self.butSpat)


        self.butNove = self.ids.btnNove
        self.butPouzit = self.ids.btnPouzit
        self.butNove.disabled = True
        self.butPouzit.disabled = True
        # self.zadanyKod = TextInput(text='', size_hint_y=None, height='48dp',
        #                       pos_hint={'center_y': 0.25})
        # self.add_widget(self.zadanyKod)
        self.zadanyKod = self.ids.input

        Clock.schedule_interval(self.read_text, 1)

    def zapnutieKamery(self, *args):
        if self.prveSpustenie:
            self.prveSpustenie = False
            self.skenovat = False
            return
        # self.add_widget(self.zbarcam)
        self.zadanyKod.text = ''
        self.skenovat = True
        self.zbarcam.start()

    def pokracovat(self, *args):
        self.skenovat = True
        #self.i = (self.i+1)%2
        #self.zbarcam.start()
        self.precButtonyKody()

    def precButtonyKody(self):
        if self.butNove is None:
            return
        # self.remove_widget(self.butNove)
        # self.remove_widget(self.butPouzit)
        # self.butNove = None
        # self.butPouzit = None
        self.butNove.disabled = True
        self.butPouzit.disabled = True

    def spat(self, *args):
        self.zbarcam.stop()
        self.remove_widget(self.zbarcam)
        self.skenovat = False
        self.precButtonyKody()
        kod = self.zadanyKod.text.strip()
        if kod:
            self.kody.append(kod)
        self.screenManager.current = self.povodnaScreen

    def koniec(self, *args):
        self.kody.clear()
        self.kody.append(self.najdene)
        self.zbarcam.stop()
        self.remove_widget(self.zbarcam)
        self.precButtonyKody()

        self.screenManager.current = self.dalsiaScreen

    def pouzitKod(self, kod):
        #self.zbarcam.stop()
        self.skenovat = False
        self.najdene = kod

        # self.butPouzit = Button(text=f'{kod}', size_hint_y=None, height='48dp', on_press=self.koniec,
        #                         pos_hint={'center_y': 0.15})
        # self.add_widget(self.butPouzit)
        # self.butNove = Button(text=f'skenovat dalej', size_hint_y=None, height='48dp', on_press=self.pokracovat,
        #                       pos_hint={'center_y': 0.25})
        # self.add_widget(self.butNove)

        self.butNove.disabled = False
        self.butPouzit.disabled = False
        self.butNove.text = f'skenovat dalej'
        self.butPouzit.text = f'{kod}'



    def read_text(self, *args):
        if self.zbarcam is None or not self.skenovat:
            return

        if self.zbarcam.symbols: # when something is detected
            self.pouzitKod(str(self.zbarcam.symbols[0].data, 'UTF-8'))
            #Clock.unschedule(self.read_qr_text, 1)
            #self.zbarcam.stop() # stop zbarcam
            #sposobuje crash na androide #self.zbarcam.ids['xcamera']._camera._device.release() # release camera
            #self.remove_widget(self.zbarcam)
            #Zobrazenie vysledku - v produkcii sa odstráni
            #vysledok = Label(text=str(self.qr_text))
            #self.add_widget(vysledok)
            #self.skenovat = False

            #self.butPouzit = Button(text=f'{self.najdene}', size_hint_y=None, height='48dp', on_press=self.koniec,
            #                        pos_hint={'center_y': 0.15})
            #self.add_widget(self.butPouzit)
            #self.butNove = Button(text=f'skenovat dalej', size_hint_y=None, height='48dp', on_press=self.pokracovat,
            #                      pos_hint={'center_y': 0.25})
            #self.add_widget(self.butNove)
        else: #pre testovanie na pocitaci
            self.pouzitKod(input("zadaj naskenovany kod: "))
