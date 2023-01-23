from kivy.uix.button import Button
#from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer,Stillage_type,Pattern_Item,Pattern
class Edit_Patterns (BoxLayout):
    """
    uprava paternov
    """
    select_customer = None
    select_pattern  = None
    select_stillage_type = None
    on_delete_type_stillage = None
    select_number = None
    notify = Button(text = '')
    drop2 = DropDown()
    drop3 = DropDown()
    drop4 = DropDown()
    drop5 = DropDown()
    mainbutton4 = Button(text='Zoznam vybratých typov vozíkov', size_hint=(.5, .25), pos=(60, 20))
    mainbutton4.bind(on_release=drop4.open)
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    btn3 = Button(text="Pridaj položku")
    btn4 = Button(text="Odstráň položku")
    customer_list = None
    stillage_type_list = None
    pattern_item_list = dict()
    pattern_list = None
    old_pattern_item_list = dict()
    Edit_data = None
    screenManager = None
    values1 = []
    values2 = []
    values3 = []
    values4 = []
    def __init__(self,screenManager, **kwargs):
        self.screenManager = screenManager
        super(Edit_Patterns, self).__init__(**kwargs)
        self.values3 = []
        for i in range (1,100):
            self.values3.append(str(i))
        self.ids.spinner_edit_pattern_3.values = self.values3
        self.notify = self.ids.notify
    def synchronize_customers(self):
        """
        natiahne zakaznikov z databazy
        """
        self.select_customer = None
        self.values1 = []
        self.customer_list = dict([(i['Name'],i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            if self.customer_list[i] in self.pattern_list.values():
                self.values1.append(i)
        self.ids.spinner_edit_pattern_1.text = "Zákazník"
        self.ids.spinner_edit_pattern_1.values = self.values1
    def synchronize_stillage_types(self):
        """
        natiahne typy vozikov z databazy
        """
        self.select_stillage_type = None
        self.values2 = []
        self.ids.spinner_edit_pattern_2.text = "Typ vozíka"
        self.stillage_type_list = dict([(i['Name'], i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.stillage_type_list:
            self.values2.append(i)
        self.ids.spinner_edit_pattern_2.values = self.values2
    def synchronize_pattern_list(self):
        """
        natiahne patternov z databazy
        """
        self.select_pattern = None
        self.pattern_list = dict([(i['id'], i['Customer_id']) for i in Pattern().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.Edit_data = Pattern().Data_on_editing()
    def clear_choosed_items(self):
        """
        zoznam vybratych stillage types patternu sa vycisti
        """
        self.values4 = []
        self.ids.spinner_edit_pattern_4.text = "Zoznam vybratých typov vozíkov"
        self.ids.spinner_edit_pattern_4.values = []
        self.on_delete_type_stillage = None
        self.pattern_item_list = dict()
    def set_customer_id(self,tex1):
        """
        oznaci vybrateho zakaznika a nacita jeho pattern
        """
        if tex1 not in self.customer_list.keys():
            return
        self.clear_choosed_items()
        self.select_pattern = None

        self.select_customer = self.customer_list[tex1]
        for i in Pattern().vrat_vsetky():
            if i['doplnok'] != 'DELETED' and i['Customer_id'] == self.select_customer:
                self.select_pattern = i['id']
                break
        self.set_widgets(self.select_pattern)
    def set_number(self,text):
        """
        ulozi pocet oznaceneho typu vozika
        """
        if text == "Počet":
            self.select_number = None
        else:
            self.select_number = text
    def set_stillage_type(self,text):
        """
        oznaci vybraty typ vozika
        """
        if text == 'Typ vozíka':
            self.select_stillage_type = None
        else:
            self.select_stillage_type = text
    def set_widgets(self,tex1):
        """
        oznaci vybrateho zakaznika
        """
        self.clear_choosed_items()
        self.select_pattern = tex1
        self.values4 = []
        for i in self.Edit_data:
            if  i[1] == self.select_customer and tex1 == i[5]:
                self.pattern_item_list.update({i[17]:str(i[10])})
                self.old_pattern_item_list.update({i[17]: str(i[10])})
                self.values4.append(i[17] + " " + str(i[10]))
        self.ids.spinner_edit_pattern_4.values = self.values4
    def set_on_delete_type_stillage(self,tex):
        """
        oznaci vyrbaty typ vozika ktory chceme z patternu zmazat
        """
        if tex == 'Zoznam vybratých typov vozíkov':
            self.on_delete_type_stillage = None
        else:
            self.on_delete_type_stillage = tex
        print(self.on_delete_type_stillage)
    def call_Back (self):
        """
        vrati sa na predchadzajucu obrazovku
        """
        self.screenManager.current = 'Settings_Patterns'
    def check_deleted_pattern_item(self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne odstrani typ vozika ktory necheme mat v paterne
        """
        if self.on_delete_type_stillage is None:
            self.notify.text = "Vyber typ vozíka na mazanie"
        else:
            self.values4 = []
            self.pattern_item_list.pop(self.on_delete_type_stillage.split()[0])
            self.ids.spinner_edit_pattern_4.text = 'Zoznam vybratých typov vozíkov'
            for i in self.pattern_item_list:
                self.values4.append(i + " " + self.pattern_item_list[i])
            self.ids.spinner_edit_pattern_4.values = self.values4
            self.on_delete_type_stillage = None
    def check_added_pattern_item(self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne prida typ vozika aj s poctom do nasho patternu
        """
        if self.select_stillage_type is None:
            self.notify.text = "Vyber typ vozíka"
        elif self.select_number is None:
            self.notify.text = "Vyber počet vozíkov daného typu"
        else:
            self.pattern_item_list.update({self.select_stillage_type:self.select_number})
            self.ids.spinner_edit_pattern_2.text = "Typ vozíka"
            self.ids.spinner_edit_pattern_3.text = "Počet"
            self.select_number = None
            self.select_stillage_type = None
        self.values4 = []
        self.ids.spinner_edit_pattern_4.values = []
        self.ids.spinner_edit_pattern_4.text = "Zoznam vybratých typov vozíkov"
        self.on_delete_type_stillage = None
        for i in self.pattern_item_list:
            self.values4.append(i + " " + self.pattern_item_list[i])
        self.ids.spinner_edit_pattern_4.values = self.values4
    def check (self):
        """
        skontroluje ci su vsetky vstupy spravne nasledne prida patern do databazy
        """
        if self.select_customer is None:
            self.notify.text = "Vyberte zákazníka"
        elif len(self.pattern_item_list) ==0:
            self.notify.text = "Vyberte typ vozíka"
        else:
            for i in self.Edit_data:
                if i[5] == self.select_pattern:
                    if i[17] in self.old_pattern_item_list.keys() and i[17] in self.pattern_item_list.keys():
                        on_update = Pattern_Item().stiahni(i[11])
                        on_update.Number = self.pattern_item_list[i[17]]
                        on_update.update()
                        self.pattern_item_list.pop(i[17])
                    elif i[17] in self.old_pattern_item_list.keys() and i[17] not in self.pattern_item_list.keys():
                        on_update = Pattern_Item().stiahni(i[11])
                        on_update.zmazat()
            for i in self.pattern_item_list:
                Pattern_Item().nahraj(int(self.pattern_item_list[i]),self.select_pattern,self.stillage_type_list[i])
            self.call_Back()
    def clear_screen(self, *args):
        """
        nacitanie udajov
        """
        self.notify.text = ""
        self.synchronize_pattern_list()
        self.synchronize_customers()
        self.synchronize_stillage_types()
        self.select_number = None
        self.ids.spinner_edit_pattern_3.text = "Počet"
        self.clear_choosed_items()
        self.old_pattern_item_list = dict()