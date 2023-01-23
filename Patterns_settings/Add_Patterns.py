from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer,Stillage_type,Pattern_Item,Pattern
class Add_Patterns (BoxLayout):
    """
    pridavanie paternov
    """
    select_customer_id  = None
    select_stillage_type = None
    on_delete_type_stillage = None
    select_number = None
    notify = Button(text = '')
    drop1 = DropDown()
    drop2 = DropDown()
    drop3 = DropDown()
    drop4 = DropDown()
    mainbutton4 = Button(text='Zoznam vybratých typov vozíkov', size_hint=(.5, .25), pos=(60, 20))
    mainbutton4.bind(on_release=drop4.open)
    btn1 = Button(text="Pridaj")
    btn2 = Button(text="Späť")
    btn3 = Button(text="Pridaj položku")
    btn4 = Button(text="Odstráň položku")
    customer_list = None
    stillage_type_list = None
    pattern_item_list = dict()
    screenManager = None
    values1=[]
    values2 = []
    values3 = []
    values4 = []
    def __init__(self,screenManager, **kwargs):
        super(Add_Patterns, self).__init__(**kwargs)
        self.screenManager = screenManager
        for i in range (1,100):
            self.values3.append(str(i))
        self.ids.spinner_add_pattern_3.values = self.values3
        self.ids.spinner_add_pattern_3.text = "Počet"
        self.drop4 = self.ids.spinner_add_pattern_4
        self.notify = self.ids.notify
    def synchronize_customers(self):
        """
        natiahne zakaznikov z databazy
        """
        self.select_customer_id = None
        self.values1 = []
        self.customer_list = dict([(i['Name'], i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED' and i['id'] not in [i['Customer_id'] for i in Pattern().vrat_vsetky() if i['doplnok'] != 'DELETED']])
        for i in self.customer_list:
            self.values1.append(i)
        self.ids.spinner_add_pattern_1.values = self.values1
        self.ids.spinner_add_pattern_1.text = "Vyber zákazníka"
    def synchronize_stillage_types(self):
        """
        natiahne typy vozikov z databazy
        """
        self.select_stillage_type = None
        # self.drop2.clear_widgets()
        self.values2 = []
        self.stillage_type_list = dict([(i['Name'], i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.stillage_type_list:
            self.values2.append(i)
        self.ids.spinner_add_pattern_2.values = self.values2
        self.ids.spinner_add_pattern_2.text = 'Typ vozíka'
        self.ids.spinner_add_pattern_3.text = 'Počet'
    def set_number(self,text):
        """
        ulozi pocet oznaceneho typu vozika
        """
        self.select_number = text
    def set_stillage_type(self,text):
        """
        oznaci vybraty typ vozika
        """
        self.select_stillage_type = text
    def set_widgets(self,tex1):
        """
        oznaci vybrateho zakaznika
        """
        if tex1 not in self.customer_list:
            return
        self.select_customer_id = self.customer_list[tex1]
    def set_on_delete_type_stillage(self,tex):
        """
        oznaci vyrbaty typ vozika ktory chceme z patternu zmazat
        """
        self.on_delete_type_stillage = tex
    def call_Back (self):
        """
        vrati sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Patterns'
    def check_deleted_pattern_tem(self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne odstrani typ vozika ktory necheme mat v paterne
        """
        if self.on_delete_type_stillage is None:
            self.notify.text = "Vyber typ vozíka na mazanie"
        else:
            self.values4 = []
            self.pattern_item_list.pop(self.on_delete_type_stillage.split()[0])
            for i in self.pattern_item_list:
                self.values4.append(i + " " + self.pattern_item_list[i])
            self.ids.spinner_add_pattern_4.values = self.values4
            self.ids.spinner_add_pattern_4.text = 'Zoznam vybratych typov vozíkov'
            self.on_delete_type_stillage = None
    def check_added_pattern_item(self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne prida typ vozika aj s poctom do nasho patternu
        """
        if self.select_customer_id is None:
            self.notify.text = "Vyber zákazníka"
        elif self.select_stillage_type is None:
            self.notify.text = "Vyber typ vozíka"
        elif self.select_number is None:
            self.notify.text = "Vyber počet vozíkov daného typu"
        else:
            self.pattern_item_list.update({self.select_stillage_type:self.select_number})
            self.ids.spinner_add_pattern_2.text = 'Typ vozíka'
            self.ids.spinner_add_pattern_3.text = 'Počet'
            self.select_number = None
            self.select_stillage_type = None
        self.values4 = []
        for i in self.pattern_item_list:
            self.values4.append(i + " " + self.pattern_item_list[i])
        self.ids.spinner_add_pattern_4.values = self.values4
        self.ids.spinner_add_pattern_4.text = 'Zoznam vybratých typov vozíkov'
    def check (self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne prida patern do databazy
        """
        if self.select_customer_id is None:
            self.notify.text = "Vyber zákazníka"
        elif len(self.pattern_item_list) ==0:
            self.notify.text = "Pridaj typ vozíka"
        else:
            Updated_Pattern_id = Pattern().nahraj(self.select_customer_id).id
            for i in self.pattern_item_list:
                Pattern_Item().nahraj(int(self.pattern_item_list[i]),Updated_Pattern_id,self.stillage_type_list[i])
            self.call_Back()
    def clear_screen(self, *args):
        """
        nacitanie udajov
        """
        self.notify.text = ""
        self.select_number = None
        self.drop3.select('Number')
        self.values4 = []
        self.drop4.values = self.values4
        self.drop4.text = "Zoznam vybratých typov vozíkov"
        self.pattern_item_list = dict()
        self.on_delete_type_stillage = None
        self.synchronize_customers()
        self.synchronize_stillage_types()
