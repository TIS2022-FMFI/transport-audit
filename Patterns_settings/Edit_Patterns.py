from scanner import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.app import App
from sqlite import Customer,Stillage_type,Pattern_Item,Pattern
class Edit_Patterns (BoxLayout):
    select_customer = None
    select_pattern  = None
    select_stillage_type = None
    on_delete_type_stillage = None
    select_number = None
    notify = Button(text = '')
    drop1 = DropDown()
    drop2 = DropDown()
    drop3 = DropDown()
    drop4 = DropDown()
    drop5 = DropDown()
    mainbutton4 = Button(text='Zoznam vybratych stillage_types', size_hint=(.5, .25), pos=(60, 20))
    mainbutton4.bind(on_release=drop4.open)
    btn1 = Button(text="Uprav")
    btn2 = Button(text="Späť")
    btn3 = Button(text="Pridaj polozku")
    btn4 = Button(text="Odstran polozku")
    customer_list = None
    stillage_type_list = None
    pattern_item_list = dict()
    pattern_list = None
    old_pattern_item_list = dict()
    Edit_data = None
    screenManager = None
    def __init__(self,screenManager, **kwargs):
        self.screenManager = screenManager
        super(Edit_Patterns, self).__init__(**kwargs)
        for i in range (1,100):
            btn = Button(text= str(i), size_hint_y=None, height=40, on_release=lambda btn: self.set_number(btn.text))
            btn.bind(on_release=lambda btn: self.drop3.select(btn.text))
            self.drop3.add_widget(btn)
        mainbutton1 = Button(text='Vyber pattern', size_hint=(.5, .25), pos=(60, 20))
        mainbutton1.bind(on_release=self.drop1.open)
        mainbutton2 = Button(text='Stillage_type', size_hint=(.5, .25), pos=(60, 20))
        mainbutton2.bind(on_release=self.drop2.open)
        mainbutton3 = Button(text='Number', size_hint=(.5, .25), pos=(60, 20))
        mainbutton3.bind(on_release=self.drop3.open)
        mainbutton5 = Button(text='Customer', size_hint=(.5, .25), pos=(60, 20))
        mainbutton5.bind(on_release=self.drop5.open)
        self.drop1.bind(on_select=lambda instance, x: setattr(mainbutton1, 'text', x))
        self.drop2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))
        self.drop3.bind(on_select=lambda instance, x: setattr(mainbutton3, 'text', x))
        self.drop4.bind(on_select=lambda instance, x: setattr(self.mainbutton4, 'text', x))
        self.drop5.bind(on_select=lambda instance, x: setattr(mainbutton5, 'text', x))
        self.btn1.bind(on_release = lambda btn:self.check())
        self.btn2.bind(on_release=lambda btn: self.call_Back())
        self.btn3.bind(on_release=lambda btn: self.check_added_pattern_item())
        self.btn4.bind(on_release=lambda btn: self.check_deleted_pattern_item())
        self.add_widget(mainbutton5)
        self.add_widget(mainbutton1)
        self.add_widget(mainbutton2)
        self.add_widget(mainbutton3)
        self.add_widget(self.btn3)
        self.add_widget(self.mainbutton4)
        self.add_widget(self.btn4)
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
        self.add_widget(self.notify)
    def synchronize_customers(self):
        self.select_customer = None
        self.drop5.clear_widgets()
        self.drop5.select('Customer')
        self.customer_list = dict([(i['Name'],i['id']) for i in Customer().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.customer_list:
            if self.customer_list[i] in self.pattern_list.values():
                btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_customer_id(btn.text))
                btn.bind(on_release=lambda btn: self.drop5.select(btn.text))
                self.drop5.add_widget(btn)
    def synchronize_stillage_types(self):
        self.select_stillage_type = None
        self.drop2.clear_widgets()
        self.drop2.select("Stillage type")
        self.stillage_type_list = dict([(i['Name'], i['id']) for i in Stillage_type().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        for i in self.stillage_type_list:
            btn = Button(text= i, size_hint_y=None, height=40, on_release=lambda btn: self.set_stillage_type(btn.text))
            btn.bind(on_release=lambda btn: self.drop2.select(btn.text))
            self.drop2.add_widget(btn)
    def synchronize_pattern_list(self):
        self.select_pattern = None
        self.pattern_list = dict([(i['id'], i['Customer_id']) for i in Pattern().vrat_vsetky() if i['doplnok'] != 'DELETED'])
        self.Edit_data = Pattern().Data_on_editing()
        self.drop1.clear_widgets()
        self.drop1.select("Vyber pattern")
    def clear_choosed_items(self):
        self.drop4.clear_widgets()
        self.drop4.select('Zoznam vybratych stillage_types')
        self.on_delete_type_stillage = None
        self.pattern_item_list = dict()
    def set_customer_id(self,tex1):
        # cistenie
        self.clear_choosed_items()
        self.select_pattern = None
        self.drop1.clear_widgets()
        self.drop1.select("Vyber pattern")

        self.select_customer = self.customer_list[tex1]
        list_of_patterns=[]
        for i in self.Edit_data:
            if  i[1] == self.select_customer and i[5] not in list_of_patterns:
                list_of_patterns.append(i[5])
                btn = Button(text= i[5], size_hint_y=None, height=40, on_release=lambda btn: self.set_widgets(btn.text))
                btn.bind(on_release=lambda btn: self.drop1.select(btn.text))
                self.drop1.add_widget(btn)
    def set_number(self,text):
        self.select_number = text
    def set_stillage_type(self,text):
        self.select_stillage_type = text
    def set_widgets(self,tex1):
        self.clear_choosed_items()
        self.select_pattern = tex1
        for i in self.Edit_data:
            if  i[1] == self.select_customer and tex1 == i[5]:
                self.pattern_item_list.update({i[17]:str(i[10])})
                self.old_pattern_item_list.update({i[17]: str(i[10])})
                btn = Button(text=i[17] + " " + str(i[10]), size_hint_y=None, height=40,on_release=lambda btn: self.set_on_delete_type_stillage(btn.text))
                btn.bind(on_release=lambda btn: self.drop4.select(btn.text))
                self.drop4.add_widget(btn)
    def set_on_delete_type_stillage(self,tex):
        self.on_delete_type_stillage = tex
    def call_Back (self):
        self.screenManager.current = 'Settings_Patterns'
    def check_deleted_pattern_item(self):
        if self.on_delete_type_stillage is None:
            self.notify.text = "Please select item to delete"
        else:
            self.drop4.clear_widgets()
            self.drop4.select('Zoznam vybratych stillage_types')
            self.pattern_item_list.pop(self.on_delete_type_stillage.split()[0])
            self.drop4.bind(on_select=lambda instance, x: setattr(self.mainbutton4, 'text', x))
            for i in self.pattern_item_list:
                btn = Button(text=i + " " + self.pattern_item_list[i], size_hint_y=None, height=40,
                             on_release=lambda btn: self.set_on_delete_type_stillage(btn.text))
                btn.bind(on_release=lambda btn: self.drop4.select(btn.text))
                self.drop4.add_widget(btn)
            self.on_delete_type_stillage = None
    def check_added_pattern_item(self):
        if self.select_pattern is None:
            self.notify.text = "Please select pattern you want edit"
        elif self.select_stillage_type is None:
            self.notify.text = "Please select stillage type you want add to pattern"
        elif self.select_number is None:
            self.notify.text = "Please select number of stillage type you want add to pattern"
        else:
            self.pattern_item_list.update({self.select_stillage_type:self.select_number})
            self.drop2.select('Stillage_type')
            self.drop3.select('Number')
            self.select_number = None
            self.select_stillage_type = None
        self.drop4.clear_widgets()
        self.drop4.select('Zoznam vybratych stillage_types')
        self.on_delete_type_stillage = None
        for i in self.pattern_item_list:
            btn = Button(text=i + " " + self.pattern_item_list[i], size_hint_y=None, height=40, on_release=lambda btn: self.set_on_delete_type_stillage(btn.text))
            btn.bind(on_release=lambda btn: self.drop4.select(btn.text))
            self.drop4.add_widget(btn)
    def check (self):
        if self.select_customer is None:
            self.notify.text = "Please choose customer"
        elif self.select_pattern is None:
            self.notify.text = "Please choose pattern"
        elif len(self.pattern_item_list) ==0:
            self.notify.text = "Add stillage_type"
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
        self.notify.text = ""
        self.synchronize_pattern_list()
        self.synchronize_customers()
        self.synchronize_stillage_types()
        self.select_number = None
        self.drop3.select("Number")
        self.clear_choosed_items()
        self.old_pattern_item_list = dict()