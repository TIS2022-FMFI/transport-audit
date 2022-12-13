from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from skener import Scanner
from UzavretyAudit import UzavretyKamion
from sqlite import Shipment, Pattern, Pattern_Item, Stillage_type
class PrebiehajuciAudit(Screen):
    def __init__(self, aplikacia, povodna, zakaznik, auto, **kwargs):
        super().__init__(**kwargs)
        self.aplikacia = aplikacia
        self.povodna = povodna
        self.zakaznik = zakaznik
        self.auto = auto
        self.vozik = None
        self.prvy = None
        self.druhy = None
        self.kod = []

        #self.uzavretaScreen = dalsia

        bSpat = Button(text='Spat', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 0.5, "top":0.2}, size_hint =(0.3, 0.08))
        bSpat.bind(on_press=self.spat)
        self.add_widget(bSpat) #upravit, toto je len na skusku
        bUzavriet = Button(text='Uzavriet kamion', pos_hint={"top":0.1, 'center_x': 0.5}, background_color="#0003a8",
                                    background_normal="",size_hint =(0.3, 0.08))
        bUzavriet.bind(on_press=self.uzavriet)
        self.add_widget(bUzavriet)

        self.skenovanieScreen = Scanner(self.aplikacia.screenManager, self.kod, self.name, self.name,
                                        name='skener' + self.name)
        self.aplikacia.screenManager.add_widget(self.skenovanieScreen)

        self.uzavretyScreen = UzavretyKamion(self.aplikacia, self, self.povodna, name='uzavrety'+self.name)
        self.aplikacia.screenManager.add_widget(self.uzavretyScreen)

        self.bVozik = Button(text='Naskenujte vozik', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.65}, size_hint=(0.3, 0.08))
        self.bVozik.bind(on_press = self.skenVozik)
        self.add_widget(self.bVozik)

        self.lVozik = Label(text='kod vozika', pos_hint={'center_x': 0.8, "top": 0.65}, size_hint=(0.5, 0.08))
        self.add_widget(self.lVozik)

        self.bPrvy = Button(text='Naskenujte prvy produkt', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.55}, size_hint=(0.3, 0.08))
        # Label(text='Nepodarilo sa najst zamestnanca s naskenovanym kodom')
        self.add_widget(self.bPrvy)

        self.lPrvy = Label(text='kod prvy', pos_hint={'center_x': 0.8, "top": 0.55}, size_hint=(0.5, 0.08))
        self.add_widget(self.lPrvy)
        self.bDruhy = Button(text='Naskenujte druhy produkt', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.45}, size_hint=(0.3, 0.08))
        # Label(text='Nepodarilo sa najst zamestnanca s naskenovanym kodom')
        self.add_widget(self.bDruhy)
        self.lDruhy = Label(text='kod druhy', pos_hint={'center_x': 0.8, "top": 0.45}, size_hint=(0.5, 0.08))
        self.add_widget(self.lDruhy)
        self.skenovanieScreen.prveSpustenie = False

        self.bind(on_enter = self.kontrolaKodu)
        self.pattern = Pattern().patternZakaznika(self.zakaznik.id)

        if self.pattern is None:
            self.spat()
        self.polozkyPatternu = Pattern_Item().vrat_vsetkyPattern(self.pattern.id)
        pouzStillage = set()
        self.polozkyPatternuDict = {}
        from random import randint
        self.maxDielikov = 0
        for p in self.polozkyPatternu:
            if p.Stillage_type_id not in pouzStillage:
                pouzStillage.add(p.Stillage_type_id)
                if p.Number == 0:
                    p.Number = randint(1, 5)

                stillageTupe = Stillage_type().stiahni(p.Stillage_type_id)
                if stillageTupe is None:
                    continue
                self.maxDielikov += p.Number
                self.polozkyPatternuDict[stillageTupe.Name] = {'item':p, 'type':stillageTupe}

        #print(Stillage_type().vrat_vsetky())
        self.sirka = 800

        self.sirkaDielika = self.sirka / self.maxDielikov
        self.dielikov = 0
        print(self.size, "sffklsjflajflafjl")
        with self.canvas:
            Color(0.4, 0.4, 0.4)
            Rectangle(pos=(0, 450), size=(self.sirka, 70))
        self.nakresliObdznik()


        self.aplikacia.audit = Shipment()


    def nakresliObdznik(self):
        if self.dielikov > self.maxDielikov:
            with self.canvas:
                Color(1, 0, 0)
                Rectangle(pos=(0, 450), size=(self.sirka, 70))
            return
        with self.canvas:
            Color(0, 1, 0)
            Rectangle(pos=(0, 450), size=(self.dielikov* self.sirkaDielika, 70))

    def spat(self, *args):
        self.aplikacia.screenManager.remove_widget(self)
        self.aplikacia.screenManager.remove_widget(self.skenovanieScreen)
        self.aplikacia.screenManager.remove_widget(self.uzavretyScreen)
        self.aplikacia.screenManager.current = self.povodna.name

    def uzavriet(self, *args):
        self.aplikacia.screenManager.current = self.uzavretyScreen.name

    def kontrolaKodu(self, *args):
        if not self.kod:
            return
        self.dielikov += 1
        self.nakresliObdznik()
        self.lVozik.text = self.kod[0]
        self.kod.clear()

    def skenVozik(self, *args):
        self.aplikacia.screenManager.current = self.skenovanieScreen.name





