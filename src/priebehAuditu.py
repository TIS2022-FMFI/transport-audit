

from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.utils import rgba

from sqlite import Shipment, Pattern, Pattern_Item, Stillage_type, Stillage, User, User_Role

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
        self.prebiehaAudit = False
        self.chyba  = False

        self.bind(on_enter = self.kontrolaKodu)



    def nakresliObdznik(self):
        """
            zobrazovanie ukazovatela naplnenia patternu
            podla toho kolko vozikov je nalozenych sa sfarbuju jednotlive dieliky
        """
        self.remove_widget(self.BL)
        self.BL = BoxLayout(pos_hint={'center_x': 0.5, "top": 1}, size_hint=(1, 0.08), orientation='horizontal')

        if self.dielikov <= self.maxDielikov:
            for i in range(self.dielikov):
                self.BL.add_widget(Button(size_hint=(1 / self.maxDielikov, 1), background_color=[0, 1, 0]))
            for i in range(self.maxDielikov - self.dielikov):
                self.BL.add_widget(Button(size_hint=(1 / self.maxDielikov, 1)))
        elif self.dielikov > self.maxDielikov:
            for i in range(self.maxDielikov):
                self.BL.add_widget(Button(size_hint=(1 / self.maxDielikov, 1), background_color=[1, 0, 0]))
        self.add_widget(self.BL)


    def spat(self, *args):
        """
            navrat na uvod auditu, aplikacia si dalej nebude pamatat udaje tohto konkretneho auditu
        """

        if self.kodNaSkenovanie == NajblizsiKod.KONTROLOR:
            self.remove_widget(self.bPotvrditVozik)
        if self.chyba:
            self.chyba = False
            self.remove_widget(self.bOdlozitOpravu)
            self.remove_widget(self.bPotvrditChybu)
        print("navrat na uvod auditu")
        self.vynulovatVozik()
        self.aplikacia.shippment = None
        self.prebiehaAudit = False
        self.aplikacia.shippmentStillages = set()
        self.aplikacia.kod.clear()
        self.pattern = None
        self.kodNaSkenovanie = NajblizsiKod.VOZIK
        self.aplikacia.screenManager.current = self.povodna.name

    def vynulovatVozik(self, *args):
        """
            labely pre skenovane hodnoty idu do povodneho stavu s praznym textom
            nastavenie do stavu kde ideme od zaciatku skenovat cely vozik
        """
        self.aplikacia.kod.clear()
        self.lVozik.text = ""
        self.lStillage.text = ""
        self.lRange.text = ""
        self.lPrvy.text = ""
        self.lDruhy.text = ""
        self.kodNaSkenovanie = NajblizsiKod.VOZIK
        self.stillage = Stillage()
        self.opravovany = False

    def uzavriet(self, *args):
        """
            preonutie sa na screen uzavreteho kamionu
        """
        self.aplikacia.screenManager.current = self.aplikacia.uzavretyScreen.name
    def kontrolaVozika(self):
        """
            kontrola udajov doskenovaneho vozika, ak vsetko sedi, rovno ho ulozime do zoznamu vozikov, ak nie zobrazia sa chybove hlasky a pridaju sa buttony na riesenie chyb
        """
        poradoveCislo = int(self.stillage.JLR_Header_NO)
        najdenaChyba = False

        if self.stillageTypMenoZKodu(self.stillage.kod) in self.poradoveCisloNasledujucehoVozikaPodlaType:
            if poradoveCislo != self.poradoveCisloNasledujucehoVozikaPodlaType[self.stillageTypMenoZKodu(self.stillage.kod)]:
                popup = Popup(title='Nájdená chyba',
                              content=Label(text=f'Nesprávne poradie vozíkov typu {self.stillageTypMenoZKodu(self.stillage.kod)}'), size_hint=(0.5, 0.5))
                popup.open()
                najdenaChyba = True
        #print("idem hladat ", self.stillage.Stillage_Number_on_Header)
        #print(self.aplikacia.udajeReportu().keys())
        dataReport = self.aplikacia.udajeReportu().get(self.stillage.Stillage_Number_on_Header, None)
        #self.report[]
        TLS = True
        if PrebiehajuciAudit.dlzkaIONO == len(self.stillage.First_scan_product):
            TLS = False
        print(dataReport)
        if dataReport is not None and dataReport:
            if TLS:
                if dataReport[0]['TLS']!= self.stillage.First_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód prvého produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if dataReport[-1]['TLS']!= self.stillage.Last_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód posledného produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
            else:
                if dataReport[0]['vehicleid']!= self.stillage.First_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód prvého produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if dataReport[-1]['vehicleid']!= self.stillage.Last_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód poslédneho produktu sa nezhoduje s reportom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
        else:
            if TLS:
                if self.stillage.TLS_range_start != self.stillage.First_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód prvého produktu sa nezhoduje s JLR headerom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
                if self.stillage.TLS_range_stop != self.stillage.Last_scan_product:
                    popup = Popup(title='Nájdená chyba',
                                  content=Label(
                                      text=f'Kód posledného produktu sa nezhoduje s JLR headerom'),
                                  size_hint=(0.5, 0.5))
                    popup.open()
                    najdenaChyba = True
            else:
                self.kodNaSkenovanie = NajblizsiKod.KONTROLOR
                self.add_widget(self.bPotvrditVozik)
                self.bVymazatVozik.disabled = True
                self.bUzavriet.disabled = True
                return
        if najdenaChyba:
            self.zobrazitChyboveButtony()
            return

        self.nahrajVozikZasielky(True)




    def nahrajVozikZasielky(self, bezChyby):
        """
            ulozenie udajov vozika do databay, podla toho ci bol chybovy alebo opravovany, nastavime prislusne hodnoty atributov
            aktualiyujeme naplnenie patternu, nasledne sa vratime do stavu kde cakame zaciatok skenovania vozika
        :param bezChyby:
        """
        if self.opravovany:
            self.aplikacia.vozikyVOprave[self.stillage.kod] = None

        poradoveCislo = int(self.stillage.JLR_Header_NO)
        self.poradoveCisloNasledujucehoVozikaPodlaType[self.stillageTypMenoZKodu(self.stillage.kod)] = poradoveCislo + 1

        self.dielikov += 1
        self.nakresliObdznik()
        self.ubratZPatternu()
        self.stillage.Date_time_end = str(parse(str(datetime.now())))
        if not bezChyby:
            self.stillage._Check = 0
            self.stillage.Note = "Expected correction"
        else:
            self.stillage._Check = 1
            if self.opravovany:
                self.stillage.Note = "Corrected"

        self.aplikacia.shippmentStillages.add(self.stillage)

        popup = Popup(title='Kontrola',
                      content=Label(text='Kontrola vozíka prebehla úspešne'), size_hint=(0.5, 0.5))
        popup.open()
        self.vynulovatVozik()

    def schovatChyboveButtony(self):
        """
            odstranenie buttonov na riesenie chyby
        """
        #upravit
        self.remove_widget(self.bPotvrditChybu)
        self.remove_widget(self.bOdlozitOpravu)
        self.bVymazatVozik.disabled = False
        self.bUzavriet.disabled = False
        print("spristupnene 1")
        #self.remove_widget(self.bVymazatVozik)

    def zobrazitChyboveButtony(self):
        """
            zobrazenie buttonov na riesenie chyb a nastavenie chybpvych atributov sicasneho vozika
        """
        #upravit
        self.chyba = True
        self.bVymazatVozik.disabled = True
        self.bUzavriet.disabled = True
        print("nepristupne buttony")
        self.stillage._Check = "NOK"
        self.stillage.Note = "Expected correction"
        self.add_widget(self.bPotvrditChybu)
        self.add_widget(self.bOdlozitOpravu)
        #self.add_widget(self.bVymazatVozik)

    def odlozitOpravu(self, *args):
        """
            chybovy vozik si dame do zoznamu cakajucich na opravenie a prepneme sa na novy vozik
        """
        #self.styllageTypeOpravaChyby.add(self.stillage.Stillage_Type_id)
        self.chyba = False
        self.bVymazatVozik.disabled = False
        self.bUzavriet.disabled = False
        print("spristupnene 2")
        self.aplikacia.vozikyVOprave[self.stillage.kod] = self.stillage
        self.schovatChyboveButtony()
        self.vynulovatVozik()
        #print(self.aplikacia.)

    def potvrditChybu(self, *args):
        """
            potvrdenie chyboveho vozika, nahranie jeho udajov
        """
        self.bVymazatVozik.disabled = False
        self.bUzavriet.disabled = False
        print("spristupnene 3")
        self.schovatChyboveButtony()
        if self.stillage.kod in self.aplikacia.vozikyVOprave:
            self.aplikacia.vozikyVOprave[self.stillage.kod] = None
        #self.styllageTypeOpravaChyby.discard(self.stillage.Stillage_Type_id)
        self.nahrajVozikZasielky(False)
        self.vynulovatVozik()

    def vyhovujeKodVozika(self, kod):
        """
        :param kod: kod na kontrolu
        :return: true ak kod vyhovuje podmienke na kod vozika, inak false
        """
        return len(kod) > 4
    def vyhovujeStillageNumberOnHeader(self, kod):
        """

        :param kod: kod na kontrolu
        :return: true ak kod vyhovuje podmienke na stillage number, inak false
        """
        return len(kod) >= 10 and kod.isnumeric()
    def vyhovujeTlsRange(self, kod):
        """

        :param kod: kod na kontrolu
        :return: true ak kod vyhovuje podmienke na tls range, inak false
        """
        if len(kod) != 9 and not "-" in kod:
            return False
        v = [x.strip() for x in kod.split("-")]
        if len(v) != 2:
            return False
        prve, druhe = v
        if len(prve) != PrebiehajuciAudit.dlzkaTLS and len(druhe) != PrebiehajuciAudit.dlzkaTLS:
            return False
        return prve.isnumeric() and druhe.isnumeric()

    def vyhovujeProdukt(self, kod):
        """
        :param kod: kod na kontrolu
        :return: true k kod ma dlzku iono alebo tls kodu a je numericky, inak false
        """
        if len(kod) != PrebiehajuciAudit.dlzkaTLS and len(kod) != PrebiehajuciAudit.dlzkaIONO:
            return False

        return kod.isnumeric()

    def stillageTypMenoZKodu(self, kod):
        """
        :param kod: kod na analyzu
        :return: meno typu vozika ktory ma vozik so zadanym kodom
        """
        return kod[:-4]

    def stillageNumberZKodu(self, kod):
        """
        :param kod: kod na analyzu
        :return: ziskany stillage number z celeho kodu z headera
        """
        return kod[-4:]

    def rozkladStillageNumberOnHeader(self, kod):
        """
        :param kod: kod z jlr headera na rozklad
        :return: jednotlive polozky kodu
        """
        vysl = {}
        vysl['carriageLabel'] = kod[3:5]
        vysl['JLRHeaderNo'] = kod[-2:]
        vysl['JLRHeaderStillageNo'] = kod[-5:].lstrip("0")
        return vysl

    def stillageTypZKodu(self, kod):
        """
        :param kod: kod na analyzu
        :return: instancia stillage type vozika so zadanym kodom
        """
        typMeno = self.stillageTypMenoZKodu(kod)
        return Stillage_type().stiahniMeno(typMeno)

    def ubratZPatternu(self):
        """
            ak je sucasny vozik v pattene, uberiem z ocakavaneho poctu vozikov jeho typu
        """
        meno = self.stillageTypMenoZKodu(self.stillage.kod)
        print(meno, self.poctyPoloziekPatternu)
        if meno in self.poctyPoloziekPatternu.keys():
            self.poctyPoloziekPatternu[meno] -= 1

    def kontrolaSplneniaPatternu(self):
        """
        :return: 1 ak je nalozenych viac vozikov ako urcuje pattern, -1 ak niektory typ z patternu nema nalozene vsetky voziky, inak 0
        """
        print(self.dielikov, self.maxDielikov)
        if self.dielikov > self.maxDielikov:
            return 1
        for st, pocet in self.poctyPoloziekPatternu.items():
            if pocet > 0:
                return -1
        return 0

    def ulozVozikKod(self):
        """
            ulozenie informacii ziskanych z kodu vozika
        """
        print("oprava ", self.aplikacia.vozikyVOprave)

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
        """
           ulozenie informacii ziskanych zo stillage number
        """
        self.stillage.Stillage_Number_on_Header = self.kodVybraty
        casti = self.rozkladStillageNumberOnHeader(self.kodVybraty)
        self.stillage.JLR_Header_NO = casti['JLRHeaderNo']
        self.stillage.Carriage_L_JLR_H = casti['carriageLabel'] + "/" + casti['JLRHeaderStillageNo']
    def ulozRange(self):
        """
            ulozenie prveho a posledneho tls kodu z jlr headera
        """
        self.stillage.TLS_range_start, self.stillage.TLS_range_stop = [x.strip() for x in self.kodVybraty.split("-")]

    def ulozPrvyKod(self):
        """
            ulozenie naskenovaneho kodu prveho produktu
        """
        self.stillage.First_scan_product = self.kodVybraty
        if len(self.kodVybraty) == PrebiehajuciAudit.dlzkaTLS:
            self.stillage.First_scan_TLS_code = self.kodVybraty

    def ulozDruhyKod(self):
        """
            ulozenie naskenovaneho kodu posledneho produktu
        """
        self.stillage.Last_scan_product = self.kodVybraty
        if len(self.kodVybraty) == PrebiehajuciAudit.dlzkaTLS:
            self.stillage.Last_scan_TLS_code = self.kodVybraty

        #self.styllageTypeOpravaChyby.discard(self.stillage.Stillage_Type_id) #doplnit do nahravania vozika

    def vynulovanieObrazovky(self, *args):
        """
            ak nie je v prebiehajuci ziaden audit, dame screen do povodneho stavu, nacitame si pattern pre zakaznika a pripravime datove struktury na kontrolu auditu
        """
        print("audit v priebehu ", self.prebiehaAudit)
        if self.prebiehaAudit:

            return

        if self.zakaznik is None:
            self.spat()
            return
        self.pattern = Pattern().patternZakaznika(self.zakaznik.id)

        if self.pattern is None:
            print("pattern je none")
            #self.spat()
            self.spat()
            return

        self.polozkyPatternu = Pattern_Item().vrat_vsetkyPattern(self.pattern.id)
        pouzStillage = set()
        self.poctyPoloziekPatternu = {}
        self.maxDielikov = 0
        for p in self.polozkyPatternu:
            if p.Stillage_type_id not in pouzStillage:
                pouzStillage.add(p.Stillage_type_id)
                stillageTupe = Stillage_type().stiahni(p.Stillage_type_id)
                if stillageTupe is None:
                    continue
                self.maxDielikov += p.Number
                self.poctyPoloziekPatternu[stillageTupe.Name] = p.Number
        print(self.poctyPoloziekPatternu)
        if self.maxDielikov == 0:
            logni(self.aplikacia.zamestnanec, 204, "pattern zakaznika je prazdny")
            self.spat()
            return

        #self.clear_widgets()
        #self.report = citaj_report_dict()
        # self.clear_widgets()

        self.bPotvrditVozik = Button(text='Potvrdiť vozík kontrolórom', background_color="#ff0000",
                                     background_normal="", pos_hint={'center_x': 0.5, "top": 0.4},
                                     size_hint=(0.5, 0.08))
        self.bPotvrditVozik.bind(on_press=self.skenKontrolor)

        self.bOdlozitOpravu = Button(text='Odložiť opravu', background_color="#ff0000",
                                     background_normal="", pos_hint={'center_x': 0.25, "top": 0.4},
                                     size_hint=(0.4, 0.08))
        self.bOdlozitOpravu.bind(on_press=self.odlozitOpravu)

        self.bPotvrditChybu = Button(text='Potvrdiť chybu', background_color="#ff0000",
                                     background_normal="", pos_hint={'center_x': 0.75, "top": 0.4},
                                     size_hint=(0.4, 0.08))
        self.bPotvrditChybu.bind(on_press=self.potvrditChybu)
        self.cervenyLabel = None

        ##########################################

        bSpat = Button(text='Zrušiť audit', background_color=rgba('#021D49'),
                       background_normal="", pos_hint={'center_x': 0.5, "top":0.3}, size_hint=(1, 0.08))
        bSpat.bind(on_press=self.spat)
        self.add_widget(bSpat)
        self.bUzavriet = Button(text='Uzavrieť kamión', pos_hint={'center_x': 0.5, "top":0.2},
                           background_color=rgba('#021D49'),
                           background_normal="", size_hint=(1, 0.08))
        self.bUzavriet.bind(on_press=self.uzavriet)
        self.add_widget(self.bUzavriet)
        self.bVymazatVozik = Button(text='Zrusiť vozík', pos_hint={'center_x': 0.5, "top":0.1},
                                    background_color=rgba('#021D49'),
                                    background_normal="", size_hint=(1, 0.08))
        self.bVymazatVozik.bind(on_press=self.vynulovatVozik)
        self.add_widget(self.bVymazatVozik)

        self.bVozik = Button(text='Vozík', background_color=rgba('#021D49'),
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.9}, size_hint=(0.5, 0.08))
        self.bVozik.bind(on_press=self.skenVozik)
        self.add_widget(self.bVozik)

        self.lVozik = Label(text='', pos_hint={'center_x': 0.8, "top": 0.9}, size_hint=(0.5, 0.08), color=[0, 0, 0])
        self.add_widget(self.lVozik)

        self.bStillage = Button(text='Stillage number', background_color=rgba('#021D49'),
                                background_normal="", pos_hint={'center_x': 0.3, "top": 0.8}, size_hint=(0.5, 0.08))
        self.bStillage.bind(on_press=self.skenStillage)
        self.add_widget(self.bStillage)
        self.lStillage = Label(text='', pos_hint={'center_x': 0.8, "top": 0.8}, size_hint=(0.5, 0.08), color=[0, 0, 0])
        self.add_widget(self.lStillage)

        self.bRange = Button(text='TLS range', background_color=rgba('#021D49'),
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.7}, size_hint=(0.5, 0.08))
        self.bRange.bind(on_press=self.skenRange)
        self.add_widget(self.bRange)
        self.lRange = Label(text='', pos_hint={'center_x': 0.8, "top": 0.7}, size_hint=(0.5, 0.08), color=[0, 0, 0])
        self.add_widget(self.lRange)

        self.bPrvy = Button(text='Prvý produkt', background_color=rgba('#021D49'),
                            background_normal="", pos_hint={'center_x': 0.3, "top": 0.6}, size_hint=(0.5, 0.08))
        self.bPrvy.bind(on_press=self.skenPrvy)
        self.add_widget(self.bPrvy)
        self.lPrvy = Label(text='', pos_hint={'center_x': 0.8, "top": 0.6}, size_hint=(0.5, 0.08), color=[0, 0, 0])
        self.add_widget(self.lPrvy)
        self.bDruhy = Button(text='Posledný produkt', background_color=rgba('#021D49'),
                             background_normal="", pos_hint={'center_x': 0.3, "top": 0.5}, size_hint=(0.5, 0.08))
        self.bDruhy.bind(on_press=self.skenDruhy)
        self.add_widget(self.bDruhy)
        self.lDruhy = Label(text='', pos_hint={'center_x': 0.8, "top": 0.5}, size_hint=(0.5, 0.08), color=[0, 0, 0])
        self.add_widget(self.lDruhy)



        self.sirka = self.size[0]

        self.sirkaDielika = self.sirka / self.maxDielikov
        self.dielikov = 0

        self.BL = BoxLayout(pos_hint={'center_x': 0.5, "top": 1}, size_hint=(1, 0.08), orientation='horizontal')

        for i in range(self.maxDielikov):
            self.BL.add_widget(Button(size_hint=(1/self.maxDielikov, 1)))
        self.add_widget(self.BL)


        self.aplikacia.shippment = Shipment()
        self.aplikacia.shippment.User_code = self.aplikacia.zamestnanec.code
        self.aplikacia.shippment.Customer_id = self.zakaznik.id
        self.aplikacia.shippment.Vehicle_id = self.auto.id

        self.aplikacia.shippmentStillages = set()
        self.poradoveCisloNasledujucehoVozikaPodlaType = {}
        self.stillage = Stillage()
        self.opravovany = False
        self.chyba = False


    def kontrolaKodu(self, *args):
        """
            ak bol prave naskenovany kod, vyhodnoti sa v zavislosti od toho, ktory typ kodu bolo povolene skenovat a vykoaju sa prislusne akcie na spracovanie kodu
        """

        self.vynulovanieObrazovky()
        print("po volani vynulovania")
        if self.pattern is None:
            print("nemame pattern")
            self.spat()
        self.aplikacia.skenovanieScreen.povodnaScreen = self.name
        self.aplikacia.skenovanieScreen.dalsiaScreen = self.name


        if not self.aplikacia.kod:
            if self.aplikacia.shippment is None:
                self.aplikacia.shippment = Shipment()
                self.aplikacia.shippment.User_code = self.aplikacia.zamestnanec.code
                self.aplikacia.shippment.Customer_id = self.zakaznik.id
                self.aplikacia.shippment.Vehicle_id = self.auto.id
            return

        self.kodVybraty = self.aplikacia.kod[0]

        if self.kodNaSkenovanie == NajblizsiKod.VOZIK:
            if self.vyhovujeKodVozika(self.kodVybraty):

                self.lVozik.text = self.kodVybraty
                self.ulozVozikKod()
                self.kodNaSkenovanie = NajblizsiKod.STILLAGE_NUMBER
        elif self.kodNaSkenovanie == NajblizsiKod.STILLAGE_NUMBER:
            if self.vyhovujeStillageNumberOnHeader(self.kodVybraty):
                self.lStillage.text = self.kodVybraty
                self.ulozStillageNumber()
                self.kodNaSkenovanie = NajblizsiKod.TLS_RANGE
        elif self.kodNaSkenovanie == NajblizsiKod.TLS_RANGE:
            if self.vyhovujeTlsRange(self.kodVybraty):
                self.lRange.text = self.kodVybraty
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
            zamestnanec = User().stiahni(self.aplikacia.kod[0])
            if zamestnanec is not None and not zamestnanec.over_zmazanie():
                rola = User_Role().stiahni(zamestnanec.User_Role_id)
                if rola is not None and not rola.over_zmazanie() and (rola.name == 'Operátor' or rola.name == 'Administrátor'):
                    self.remove_widget(self.bPotvrditVozik)
                    self.bVymazatVozik.disabled = False
                    self.bUzavriet.disabled = False
                    print("spristupnene 4")

                    self.nahrajVozikZasielky(True)
                    self.aplikacia.kod.clear()
                    return
            popup = Popup(title='Autentifikácia neprebehla',
                          content=Label(
                              text='Nebol nájdený zamestanec s naskenovaným kódom alebo nemal potrebné oprávnenie'),
                          size_hint=(0.5, 0.5))
            popup.open()

        self.aplikacia.kod.clear()

    def skenPrvy(self, *args):
        """
            ak je povolene skenovanie prveho produktu, prepneme sa na skenovaciu screen
        """
        if self.kodNaSkenovanie != NajblizsiKod.PRVY:
            return
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def skenDruhy(self, *args):
        """
            ak je povolene skenovanie posledneho produktu, prepneme sa na skenovaciu screen
        """
        if self.kodNaSkenovanie != NajblizsiKod.DRUHY:
            return
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def skenVozik(self, *args):
        """
            ak je povolene skenovanie kodu vozika, prepneme sa na skenovaciu screen
        """
        self.prebiehaAudit = True
        if self.kodNaSkenovanie != NajblizsiKod.VOZIK:
            return
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def skenStillage(self, *args):
        """
            ak je povolene skenovanie stillage number z headera, prepneme sa na skenovaciu screen
        """
        if self.kodNaSkenovanie != NajblizsiKod.STILLAGE_NUMBER:
            return
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def skenRange(self, *args):
        """
            ak je povolene skenovanie tls range z headera, prepneme sa na skenovaciu screen
        """
        if self.kodNaSkenovanie != NajblizsiKod.TLS_RANGE:
            return
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name

    def skenKontrolor(self, *args):
        """
            nastavenie na skenovanie kodu kontrolora a prepnutie na skenovaciu screen
        """
        self.kodNaSkenovanie = NajblizsiKod.KONTROLOR
        self.aplikacia.screenManager.current = self.aplikacia.skenovanieScreen.name





