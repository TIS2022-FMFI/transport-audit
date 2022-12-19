import sqlite3
import time

from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from skener import Scanner
from UzavretyAudit import UzavretyKamion
from sqlite import Shipment, Pattern, Pattern_Item, Stillage_type, Stillage

from random import randint
from enum import Enum
from datetime import datetime
from dateutil.parser import parse
class NajblizsiKod(Enum):
    VOZIK = 0
    PRVY = 1
    DRUHY = 2

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
        self.kodVybraty  =None
        self.kodNaSkenovanie = NajblizsiKod.VOZIK
        self.styllageTypeOpravaChyby = set()

        #self.uzavretaScreen = dalsia

        self.bOdlozitOpravu = Button(text='Odlozit opravu', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 0.25, "top":0.3}, size_hint =(0.3, 0.08))
        #self.add_widget(self.bOdlozitOpravu)
        self.bOdlozitOpravu.bind(on_press = self.odlozitOpravu)

        self.bPotvrditChybu = Button(text='Potvrdit chybu', background_color="#0003a8",
                                     background_normal="", pos_hint={'center_x': 0.75, "top": 0.3},
                                     size_hint=(0.3, 0.08))
        self.bPotvrditChybu.bind(on_press = self.potvrditChybu)
        #self.add_widget(self.bPotvrditChybu)
        self.cervenyLabel = None

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
        self.bPrvy.bind(on_press = self.skenPrvy)
        self.add_widget(self.bPrvy)

        self.lPrvy = Label(text='kod prvy', pos_hint={'center_x': 0.8, "top": 0.55}, size_hint=(0.5, 0.08))
        self.add_widget(self.lPrvy)
        self.bDruhy = Button(text='Naskenujte druhy produkt', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.45}, size_hint=(0.3, 0.08))
        self.bDruhy.bind(on_press=self.skenDruhy)
        self.add_widget(self.bDruhy)
        self.lDruhy = Label(text='kod druhy', pos_hint={'center_x': 0.8, "top": 0.45}, size_hint=(0.5, 0.08))
        self.add_widget(self.lDruhy)
        self.skenovanieScreen.prveSpustenie = False

        self.bind(on_enter = self.kontrolaKodu)

        self.pattern = Pattern().patternZakaznika(self.zakaznik.id)

        if self.pattern is None:
            print("pattern je none")
            #self.spat()
            return
        self.polozkyPatternu = Pattern_Item().vrat_vsetkyPattern(self.pattern.id)
        pouzStillage = set()
        self.poctyPoloziekPatternu = {}
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
                self.poctyPoloziekPatternu[stillageTupe.Name] = p.Number

        #print(Stillage_type().vrat_vsetky())
        self.sirka = 800

        self.sirkaDielika = self.sirka / self.maxDielikov
        self.dielikov = 0

        with self.canvas:
            Color(0.4, 0.4, 0.4)
            Rectangle(pos=(0, 450), size=(self.sirka, 70))
        self.nakresliObdznik()


        self.aplikacia.shippment = Shipment()
        self.aplikacia.shippment.User_code = self.aplikacia.zamestnanec.code
        self.aplikacia.shippment.Customer_id = self.zakaznik.id
        self.aplikacia.shippment.Vehicle_id = self.auto.id

        self.aplikacia.shippentStillages = set()
        self.stillage = Stillage()
        self.opravovany = False


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
        print("navrat na uvod auditu")
        self.aplikacia.shippment = None
        self.aplikacia.shippentStillages = set()
        self.aplikacia.screenManager.remove_widget(self)
        self.aplikacia.screenManager.remove_widget(self.skenovanieScreen)
        self.aplikacia.screenManager.remove_widget(self.uzavretyScreen)
        self.aplikacia.screenManager.current = self.povodna.name

    def uzavriet(self, *args):
        self.aplikacia.screenManager.current = self.uzavretyScreen.name

    def nahrajVozikZasielky(self):
        #self.stillage.nahraj()
        self.dielikov += 1
        self.nakresliObdznik()
        self.ubratZPatternu()
        self.stillage.Date_time_end = str(parse(str(datetime.now())))
        if self.stillage.Last_scan_TLS_code == self.stillage.TLS_range_stop and self.stillage.First_scan_TLS_code == self.stillage.TLS_range_start:
            self.stillage._Check = "OK"
            if self.opravovany:
                self.stillage.Note = "Corrected"
        else:
            self.stillage._Check = "NOK"
            self.stillage.Note = "Expected correction"
        self.aplikacia.shippmentStillages.add(self.stillage)
        self.stillage = Stillage()
        popup = Popup(title='Kontrola',
                      content=Label(text='Kontrola vozika prebehla uspesne'), size_hint=(0.5, 0.5))
        popup.open()

    def schovatChyboveButtony(self):

        self.remove_widget(self.bPotvrditChybu)
        self.remove_widget(self.bOdlozitOpravu)
        self.cervenyLabel.color = (1, 1, 1, 1)

    def zobrazitChyboveButtony(self):
        self.stillage._Check = "NOK"
        self.stillage.Note = "Expected correction"
        self.add_widget(self.bPotvrditChybu)
        self.add_widget(self.bOdlozitOpravu)
        self.cervenyLabel.color = (10, 0, 0, 1)
    def odlozitOpravu(self, *args):
        self.styllageTypeOpravaChyby.add(self.stillage.Stillage_Type_id)
        self.aplikacia.vozikyVOprave[self.stillage.Stillage_Number_on_Header] = self.stillage
        self.stillage = Stillage()
        self.opravovany = False
        self.schovatChyboveButtony()

        self.kodNaSkenovanie = NajblizsiKod.VOZIK
        self.lVozik.text = "kod vozik"
        self.lPrvy.text = "kod prvy"
        self.lDruhy.text = "kod druhy"
    def potvrditChybu(self, *args):
        self.schovatChyboveButtony()
        self.opravovany = True
        if self.stillage.Stillage_Number_on_Header in self.aplikacia.vozikyVOprave.keys():
            self.aplikacia.vozikyVOprave[self.stillage.Stillage_Number_on_Header] = None
        if self.kodNaSkenovanie == NajblizsiKod.VOZIK:
            self.ulozVozikKod()
        elif self.kodNaSkenovanie == NajblizsiKod.PRVY:
            self.ulozPrvyKod()
        else:
            self.ulozDruhyKod()


    def kontrolaVozik(self):
        return randint(0, 10) > 5
    def kontrolaPrveho(self):
        return randint(0, 10) > 5
    def kontrolaDruheho(self):
        return randint(0, 10) > 5

    def stillageTypMenoZKodu(self, kod):
        return kod[0:2]

    def stillageTypZKodu(self, kod):
        typMeno = self.stillageTypMenoZKodu(kod) #doplnit vytiahnutie typy voziku z kodu konkretneho voziku
        return Stillage_type().stiahniMeno(typMeno)

    def ubratZPatternu(self):
        meno = self.stillageTypMenoZKodu(self.stillage.kod)
        if meno in self.poctyPoloziekPatternu.keys():
            self.poctyPoloziekPatternu[meno] -= 1

    def kontrolaSplneniaPatternu(self):
        if self.dielikov > self.maxDielikov:
            return 1
        for st, pocet in self.poctyPoloziekPatternu.items():
            if pocet > 0:
                return -1
        return 0

    def ulozVozikKod(self):
        self.kodNaSkenovanie = NajblizsiKod.PRVY
        if self.kodVybraty in self.aplikacia.vozikyVOprave and self.aplikacia.vozikyVOprave[self.kodVybraty] is not None:
            self.opravovany = True
            self.stillage = self.aplikacia.vozikyVOprave[self.kodVybraty]
            return
        self.opravovany = False
        self.stillage.Date_time_start = str(parse(str(datetime.now())))
        self.stillage.kod = self.kodVybraty
        #self.stillage.Stillage_number = poradove cislo ziskane z kodu
        #sself.stillage.Stillage_Number_on_Header = self.kodVybraty
        #self.stillage.JLR_Header_NO = posledne dvojcislie zo stillage number on header
        #self.stillage.Carriage_L_JLR_H = tiez vytiahnut z kodu
        stType = self.stillageTypZKodu(self.kodVybraty)
        if stType is not None:
            self.stillage.Stillage_Type_id =stType.id
        else:
            self.stillage.Stillage_Type_id = None
        #self.stillage.TLS_range_start =
        #self.stillage.TLS_range_stop =
        #self.stillage.First_scan_TLS_code =
        #self.stillage.Last_scan_TLS_code =

    def ulozPrvyKod(self):
        print(self.kod, "kod")
        self.kodNaSkenovanie = NajblizsiKod.DRUHY
        self.stillage.First_scan_product = self.kodVybraty
        self.stillage.First_scan_product = self.kodVybraty

    def ulozDruhyKod(self):
        self.stillage.Last_scan_product = self.kodVybraty
        self.stillage.Last_scan_TLS_code = self.kodVybraty
        self.nahrajVozikZasielky()
        self.styllageTypeOpravaChyby.discard(self.stillage.Stillage_Type_id)
        self.kodNaSkenovanie = NajblizsiKod.VOZIK


        self.lVozik.text = "kod vozik"
        self.lPrvy.text = "kod prvy"
        self.lDruhy.text = "kod druhy"

    def kontrolaKodu(self, *args):
        if self.cervenyLabel is not None:
            self.schovatChyboveButtony()
        if self.pattern is None:
            self.spat()

        if not self.kod:
            if self.aplikacia.shippment is None:
                self.aplikacia.shippment = Shipment()
                self.aplikacia.shippment.User_code = self.aplikacia.zamestnanec.code
                self.aplikacia.shippment.Customer_id = self.zakaznik.id
                self.aplikacia.shippment.Vehicle_id = self.auto.id
            return
        self.kodVybraty = self.kod[0]
        print(self.lVozik.color)
        if self.kodNaSkenovanie == NajblizsiKod.VOZIK:
            self.lVozik.text = self.kodVybraty
            if self.kontrolaVozik():
                self.ulozVozikKod()
                self.lVozik.color = (1, 1, 1, 1)
            else:
                #self.lVozik.color = (10, 0, 0, 1)
                self.cervenyLabel = self.lVozik
                self.zobrazitChyboveButtony()

        elif self.kodNaSkenovanie == NajblizsiKod.PRVY:
            self.lPrvy.text = self.kod[0]
            if self.kontrolaPrveho():
                self.ulozPrvyKod()
                self.lPrvy.color = (1, 1, 1, 1)
            else:
                #self.lPrvy.color = (10, 0, 0, 1)
                self.cervenyLabel = self.lPrvy
                self.zobrazitChyboveButtony()

        elif self.kodNaSkenovanie == NajblizsiKod.DRUHY:
            self.lDruhy.text = self.kodVybraty
            if self.kontrolaDruheho():
                self.lDruhy.color = (1, 1, 1, 1)
                self.ulozDruhyKod()
            else:
                #self.lDruhy.color = (10, 0, 0, 1)
                self.cervenyLabel = self.lDruhy
                self.zobrazitChyboveButtony()

        self.kod.clear()

    def skenPrvy(self, *args):

        if self.kodNaSkenovanie != NajblizsiKod.PRVY:
            return
        self.aplikacia.screenManager.current = self.skenovanieScreen.name

    def skenDruhy(self, *args):
        if self.kodNaSkenovanie != NajblizsiKod.DRUHY:
            return
        self.aplikacia.screenManager.current = self.skenovanieScreen.name

    def skenVozik(self, *args):
        if self.kodNaSkenovanie != NajblizsiKod.VOZIK:
            return
        self.aplikacia.screenManager.current = self.skenovanieScreen.name





