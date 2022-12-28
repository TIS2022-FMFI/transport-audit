import sqlite3
import time

from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

from skener import Scanner
from UzavretyAudit import UzavretyKamion
from sqlite import Shipment, Pattern, Pattern_Item, Stillage_type, Stillage, User, User_Role

from random import randint
from enum import Enum
from datetime import datetime
from dateutil.parser import parse
#from parser import *
class NajblizsiKod(Enum):
    VOZIK = 0
    STILLAGE_NUMBER = 1
    TLS_RANGE = 2
    PRVY = 3
    DRUHY = 4
    KONTROLOR = 5
    ZIADEN = 6


class PrebiehajuciAudit(Screen):
    dlzkaTLS = 4
    dlzkaIONO = 8
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
        self.poradoveCisloNasledujucehoVozikaPodlaType = {}
        self.report = {} ###stiahnut si to zo spracovaneho reportu

        self.bPotvrditVozik = Button(text='Potvrdit vozik kontrolorom', background_color="#ff0000",
                                     background_normal="", pos_hint={'center_x': 0.25, "top": 0.2},
                                     size_hint=(0.5, 0.08))
        self.bPotvrditVozik.bind(on_press=self.skenKontrolor)

        self.bOdlozitOpravu = Button(text='Odlozit opravu', background_color="#ff0000",
                                    background_normal="", pos_hint = {'center_x': 0.25, "top":0.2}, size_hint =(0.3, 0.08))
        self.bOdlozitOpravu.bind(on_press = self.odlozitOpravu)

        self.bPotvrditChybu = Button(text='Potvrdit chybu', background_color="#ff0000",
                                     background_normal="", pos_hint={'center_x': 0.75, "top": 0.2},
                                     size_hint=(0.3, 0.08))
        self.bPotvrditChybu.bind(on_press = self.potvrditChybu)
        self.cervenyLabel = None

        ##########################################

        bSpat = Button(text='Spat', background_color="#0003a8",
                                    background_normal="", pos_hint = {'center_x': 5 * 1/6, "top":0.1}, size_hint =(0.3, 0.08))
        bSpat.bind(on_press=self.spat)
        self.add_widget(bSpat)
        bUzavriet = Button(text='Uzavriet kamion', pos_hint={"top":0.1, 'center_x': 3 * 1/6}, background_color="#0003a8",
                                    background_normal="",size_hint =(0.3, 0.08))
        bUzavriet.bind(on_press=self.uzavriet)
        self.add_widget(bUzavriet)
        self.bVymazatVozik = Button(text='Zrusit vozik', pos_hint={"top": 0.1, 'center_x': 1 / 6},
                           background_color="#0003a8",
                           background_normal="", size_hint=(0.3, 0.08))
        self.bVymazatVozik.bind(on_press=self.vynulovatVozik)
        self.add_widget(self.bVymazatVozik)
        #####################################

        self.skenovanieScreen = Scanner(self.aplikacia.screenManager, self.kod, self.name, self.name,
                                        name='skener' + self.name)
        self.aplikacia.screenManager.add_widget(self.skenovanieScreen)

        self.uzavretyScreen = UzavretyKamion(self.aplikacia, self, self.povodna, name='uzavrety'+self.name)
        self.aplikacia.screenManager.add_widget(self.uzavretyScreen)
        ##########################################

        self.bVozik = Button(text='Naskenujte vozik', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.75}, size_hint=(0.3, 0.08))
        self.bVozik.bind(on_press = self.skenVozik)
        self.add_widget(self.bVozik)

        self.lVozik = Label(text='kod vozika', pos_hint={'center_x': 0.8, "top": 0.75}, size_hint=(0.5, 0.08))
        self.add_widget(self.lVozik)

        self.bStillage = Button(text='Naskenujte stillage number', background_color="#0003a8",
                            background_normal="", pos_hint={'center_x': 0.3, "top": 0.65}, size_hint=(0.3, 0.08))
        self.bStillage.bind(on_press=self.skenStillage)
        self.add_widget(self.bStillage)
        self.lStillage = Label(text='stillage number', pos_hint={'center_x': 0.8, "top": 0.65}, size_hint=(0.5, 0.08))
        self.add_widget(self.lStillage)

        self.bRange = Button(text='Naskenujte TLS range', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.55}, size_hint=(0.3, 0.08))
        self.bRange.bind(on_press=self.skenRange)
        self.add_widget(self.bRange)
        self.lRange = Label(text='TLS range', pos_hint={'center_x': 0.8, "top": 0.55}, size_hint=(0.5, 0.08))
        self.add_widget(self.lRange)

        self.bPrvy = Button(text='Naskenujte prvy produkt', background_color="#0003a8",
                            background_normal="", pos_hint={'center_x': 0.3, "top": 0.45}, size_hint=(0.3, 0.08))
        self.bPrvy.bind(on_press=self.skenPrvy)
        self.add_widget(self.bPrvy)
        self.lPrvy = Label(text='kod prvy', pos_hint={'center_x': 0.8, "top": 0.45}, size_hint=(0.5, 0.08))
        self.add_widget(self.lPrvy)
        self.bDruhy = Button(text='Naskenujte druhy produkt', background_color="#0003a8",
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.35}, size_hint=(0.3, 0.08))
        self.bDruhy.bind(on_press=self.skenDruhy)
        self.add_widget(self.bDruhy)
        self.lDruhy = Label(text='kod druhy', pos_hint={'center_x': 0.8, "top": 0.35}, size_hint=(0.5, 0.08))
        self.add_widget(self.lDruhy)
        #######################
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
            Rectangle(pos=(0, 500), size=(self.sirka, 70))
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

    def vynulovatVozik(self, *args):
        self.kod.clear()
        self.lVozik.text = ""
        self.lStillage.text = ""
        self.lRange.text = ""
        self.lPrvy.text = ""
        self.lDruhy.text = ""
        self.kodNaSkenovanie = NajblizsiKod.VOZIK
        self.stillage = Stillage()
        self.opravovany = False

    def uzavriet(self, *args):
        self.aplikacia.screenManager.current = self.uzavretyScreen.name
    def kontrolaVozika(self):
        poradoveCislo = int(self.stillage.JLR_Header_NO)
        najdenaChyba = False

        if self.stillage.Stillage_Type_id in self.poradoveCisloNasledujucehoVozikaPodlaType.keys():
            if najdenaChyba != self.poradoveCisloNasledujucehoVozikaPodlaType[self.stillage.Stillage_Type_id]:
                popup = Popup(title='Najdena chyba',
                              content=Label(text=f'Nespravne poradie vozikov typu {self.stillageTypMenoZKodu(self.stillage.kod)}'), size_hint=(0.5, 0.5))
                popup.open()
                najdenaChyba = True

        dataReport = self.report[self.stillage.Stillage_Number_on_Header]
        TLS = True
        if PrebiehajuciAudit.dlzkaIONO == self.stillage.First_scan_product:
            TLS = False
        if dataReport is not None:
            if TLS:
                if dataReport[0]['TLS']!= self.stillage.First_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod prveho produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if dataReport[1]['TLS']!= self.stillage.Last_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod posledneho produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
            else:
                if dataReport[0]['asmsequence_s']!= self.stillage.First_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod prveho produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if dataReport[1]['asmsequence_s']!= self.stillage.Last_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod posledneho produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
        else:
            if TLS:
                if self.stillage.TLS_range_start != self.stillage.First_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod prveho produktu sa nezhoduje s JLR headerom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if self.stillage.TLS_range_stop != self.stillage.Last_scan_product:
                    popup = Popup(title='Najdena chyba',
                                  content=Label(
                                      text=f'Kod posledneho produktu sa nezhoduje s JLR headerom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
            else:
                self.kodNaSkenovanie = NajblizsiKod.KONTROLOR
                self.add_widget(self.bPotvrditVozik)
        if najdenaChyba:
            self.zobrazitChyboveButtony()
            return
        self.nahrajVozikZasielky(True)




    def nahrajVozikZasielky(self, bezChyby):
        ##############upravit

        poradoveCislo = int(self.stillage.JLR_Header_NO)
        self.poradoveCisloNasledujucehoVozikaPodlaType[self.stillage.Stillage_Type_id] = poradoveCislo + 1

        self.dielikov += 1
        self.nakresliObdznik()
        self.ubratZPatternu()
        self.stillage.Date_time_end = str(parse(str(datetime.now())))
        if not bezChyby:
            self.stillage._Check = "NOK"
            self.stillage.Note = "Expected correction"
        else:
            self.stillage._Check = "OK"
            if self.opravovany:
                self.stillage.Note = "Corrected"

        self.aplikacia.shippmentStillages.add(self.stillage)

        popup = Popup(title='Kontrola',
                      content=Label(text='Kontrola vozika prebehla uspesne'), size_hint=(0.5, 0.5))
        popup.open()
        self.vynulovatVozik()

    def schovatChyboveButtony(self):
        #upravit
        self.remove_widget(self.bPotvrditChybu)
        self.remove_widget(self.bOdlozitOpravu)
        self.remove_widget(self.bVymazatVozik)

    def zobrazitChyboveButtony(self):
        #upravit
        self.stillage._Check = "NOK"
        self.stillage.Note = "Expected correction"
        self.add_widget(self.bPotvrditChybu)
        self.add_widget(self.bOdlozitOpravu)
        self.add_widget(self.bVymazatVozik)

    def odlozitOpravu(self, *args):
        #self.styllageTypeOpravaChyby.add(self.stillage.Stillage_Type_id)
        self.aplikacia.vozikyVOprave[self.stillage.Stillage_Number_on_Header] = self.stillage
        self.schovatChyboveButtony()
        self.vynulovatVozik()

    def potvrditChybu(self, *args):
        self.schovatChyboveButtony()
        if self.stillage.Stillage_Number_on_Header in self.aplikacia.vozikyVOprave.keys():
            self.aplikacia.vozikyVOprave[self.stillage.Stillage_Number_on_Header] = None
        #self.styllageTypeOpravaChyby.discard(self.stillage.Stillage_Type_id)
        self.nahrajVozikZasielky(False)
        self.vynulovatVozik()


    def kontrolaVozik(self):
        return randint(0, 10) > 5
    def kontrolaPrveho(self):
        return randint(0, 10) > 5
    def kontrolaDruheho(self):
        return randint(0, 10) > 5

    def vyhovujeKodVozika(self, kod):
        return len(kod) > 4
    def vyhovujeStillageNumberOnHeader(self, kod):
        return len(kod) >= 10 and kod.isnumeric()
    def vyhovujeTlsRange(self, kod):
        if len(kod) != 9 and not "-" in kod:
            return False
        v = kod.split("-")
        if len(v) != 2:
            return False
        prve, druhe = v
        if len(prve) != PrebiehajuciAudit.dlzkaTLS and len(druhe) != PrebiehajuciAudit.dlzkaTLS:
            return False
        return prve.isnumeric() and druhe.isnumeric()

    def vyhovujeProdukt(self, kod):
        if len(kod) != PrebiehajuciAudit.dlzkaTLS or len(kod) != PrebiehajuciAudit.dlzkaIONO:
            return False
        return kod.isnumeric()

    def stillageTypMenoZKodu(self, kod):
        return kod[:-4]

    def stillageNumberZKodu(self, kod):
        return kod[-4:]

    def rozkladStillageNumberOnHeader(self, kod):
        vysl = {}
        vysl['carriageLabel'] = kod[3:5]
        vysl['JLRHeaderNo'] = kod[-2:]
        vysl['JLRHeaderStillageNo'] = kod[-5:].lstrip("0")
        return vysl

    def stillageTypZKodu(self, kod):
        typMeno = self.stillageTypMenoZKodu(kod)
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
        if self.kodVybraty in self.aplikacia.vozikyVOprave and self.aplikacia.vozikyVOprave[self.kodVybraty] is not None:
            self.opravovany = True
            self.stillage = self.aplikacia.vozikyVOprave[self.kodVybraty]
            return
        self.opravovany = False
        self.stillage.Date_time_start = str(parse(str(datetime.now())))
        self.stillage.kod = self.kodVybraty
        self.stillage.Stillage_number = self.stillageNumberZKodu(self.kodVybraty)

        stType = self.stillageTypZKodu(self.kodVybraty)
        if stType is not None:
            self.stillage.Stillage_Type_id =stType.id
        else:
            self.stillage.Stillage_Type_id = None


    def ulozStillageNumber(self):
        self.stillage.Stillage_Number_on_Header = self.kodVybraty
        casti = self.rozkladStillageNumberOnHeader(self.kodVybraty)
        self.stillage.JLR_Header_NO = casti['JLRHeaderNo']
        self.stillage.Carriage_L_JLR_H = casti['carriageLabel'] + "/" + casti['JLRHeaderStillageNo']
    def ulozRange(self):
        self.stillage.TLS_range_start, self.stillage.TLS_range_stop = self.kodVybraty.split("-")

    def ulozPrvyKod(self):
        self.stillage.First_scan_product = self.kodVybraty
        if len(self.kodVybraty) == PrebiehajuciAudit.dlzkaTLS:
            self.stillage.First_scan_TLS_code = self.kodVybraty

    def ulozDruhyKod(self):
        self.stillage.Last_scan_product = self.kodVybraty
        if len(self.kodVybraty) == PrebiehajuciAudit.dlzkaTLS:
            self.stillage.Last_scan_TLS_code = self.kodVybraty

        self.styllageTypeOpravaChyby.discard(self.stillage.Stillage_Type_id) #doplnit do nahravania vozika


    def kontrolaKodu(self, *args):
        #upravit

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

        if self.kodNaSkenovanie == NajblizsiKod.VOZIK:
            if self.vyhovujeKodVozika(self.kod):
                self.lVozik.text = self.kodVybraty
                self.ulozVozikKod()
                self.kodNaSkenovanie = NajblizsiKod.STILLAGE_NUMBER
        elif self.kodNaSkenovanie == NajblizsiKod.STILLAGE_NUMBER:
            if self.vyhovujeStillageNumberOnHeader(self.kodVybraty):
                self.lStillage = self.kodVybraty
                self.ulozStillageNumber()
                self.kodNaSkenovanie = NajblizsiKod.TLS_RANGE
        elif self.kodNaSkenovanie == NajblizsiKod.TLS_RANGE:
            if self.vyhovujeTlsRange(self.kodVybraty):
                self.lRange = self.kodVybraty
                self.ulozRange()
                self.kodNaSkenovanie = NajblizsiKod.PRVY
        elif self.kodNaSkenovanie == NajblizsiKod.PRVY:
            if self.vyhovujeProdukt(self.kodVybraty):
                self.lPrvy.text = self.kodVybraty
                self.ulozPrvyKod()
                self.kodNaSkenovanie = NajblizsiKod.DRUHY
        elif self.kodNaSkenovanie == NajblizsiKod.DRUHY:
            if self.vyhovujeProdukt(self.kodVybraty):
                self.lDruhy.text = self.kodVybraty
                self.ulozDruhyKod()
                self.kontrolaVozika()
        elif self.kodNaSkenovanie == NajblizsiKod.KONTROLOR:
            ###doplnit kontrolu koda kontrolora
            zamestnanec = User().stiahni(self.kod[0])
            if zamestnanec is not None and not zamestnanec.over_zmazanie():
                rola = User_Role().stiahni(zamestnanec.User_Role_id)
                if rola is not None and not rola.over_zmazanie() and rola.name == 'Operátor':
                    self.remove_widget(self.bPotvrditVozik)
                    self.nahrajVozikZasielky(True)
                    self.kod.clear()
                    return
            popup = Popup(title='Autentifikacia neprebehla',
                          content=Label(
                              text='Nebol najdeny zamestanec s naskenovanym kodom alebo nemal potrebne opravnenie'),
                          size_hint=(0.5, 0.5))
            popup.open()

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

    def skenStillage(self, *args):
        if self.kodNaSkenovanie != NajblizsiKod.STILLAGE_NUMBER:
            return
        self.aplikacia.screenManager.current = self.skenovanieScreen.name

    def skenRange(self, *args):
        if self.kodNaSkenovanie != NajblizsiKod.TLS_RANGE:
            return
        self.aplikacia.screenManager.current = self.skenovanieScreen.name

    def skenKontrolor(self, *args):
        self.kodNaSkenovanie = NajblizsiKod.KONTROLOR
        self.aplikacia.screenManager.current = self.skenovanieScreen.name





