import psycopg2
from sqlite import *
#pip install psycopg2
#Pred testom sa uisti, že máš najnovšiu verziu štruktúry databázy z githubu (gefco.db)
#!!!!!!!!!!!!!!!!
# Všetky dáta z lokálnej databázy budú zmazané
#!!!!!!!!!!!!!!!
# Netreba zabúdať, že test zaprace vzdialenú databázu s hlúposťami. Preto pri prevádzke by sa tento skript nemal spúšťať
conn = psycopg2.connect(
    host="server.nahovno.eu",
    database="audit-preprav",
    user="admin",
    password="Verejne_zname_heslo_47",
    options="-c search_path=public")
cur = conn.cursor()


def vyprazdni_db():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for tabulka in cursor.fetchall():
        tab = tabulka[0]
        sql = f"""DELETE FROM {tab} """
        cursor.execute(sql)
        sql = f"""SELECT COUNT(*) FROM {tab} """
        cursor.execute(sql)
        assert cursor.fetchone()[0] == 0, "Tabuľky obsahujú dáta"
    cursor.execute("COMMIT")
    cursor.execute("VACUUM")

def General_test():
    #Test nahraj
    Last_changes = str(datetime.datetime(2013, 9, 20,13,00))
    Last_available = str(datetime.datetime(2015, 10, 22, 13, 00))
    Automatic_export = True
    general = General()
    general.nahraj(Last_changes, Last_available, Automatic_export)
    assert general.Last_changes == Last_changes
    assert general.Last_available == Last_available
    assert general.Automatic_export == Automatic_export
    # Test stiahni
    general1_id = general.id
    general2 = General()
    general2.stiahni(general1_id)
    assert general2.Last_changes == Last_changes
    assert general2.Last_available == Last_available
    assert general2.Automatic_export == Automatic_export
    #Test update
    Last_changes = str(datetime.datetime(2018, 4, 20, 13, 00))
    Last_available = str(datetime.datetime(2019, 9, 21, 13, 00))
    Automatic_export = False
    general.Last_changes =  Last_changes
    general.Last_available =  Last_available
    general.Automatic_export =  Automatic_export
    general.update()
    #print(general1_id)
    general2.stiahni(general1_id)
    assert general2.Last_changes == Last_changes
    assert general2.Last_available == Last_available
    assert general2.Automatic_export == Automatic_export

def User_role_test():
    name = "Test Testovič"
    user = User_Role()
    user.nahraj(name)
    assert user.name == name
    user2 = User_Role().stiahni(user.id)
    assert user2.name == name
    #print(user2.id)
    user2.name = "Test update"
    user2.update()
    user.stiahni(user2.id)
    assert user.name == user2.name
def Customer_test():
    customer = Customer()
    Name = "CORPOS a.s"
    customer.nahraj(Name)
    assert customer.Name == Name
    customer2 = Customer().stiahni(customer.id)
    assert customer2.Name == Name
    Name = "CORPOS REFORGED"
    customer2.Name = Name
    customer2.update()
    customer.stiahni(customer2.id)
    assert customer2.Name == Name
    assert customer.Name == Name

def Vehicle_test():
    vehicle = Vehicle()
    SPZ = "TO456LM"
    vehicle.nahraj(SPZ)
    assert SPZ == vehicle.SPZ
    vehicle2 = Vehicle()
    vehicle2.stiahni(vehicle.id)
    assert vehicle2.SPZ == SPZ
    SPZ2 = "POKEMON"
    vehicle2.SPZ = SPZ2
    vehicle2.update()
    vehicle.stiahni(vehicle2.id)
    assert  vehicle2.SPZ == vehicle.SPZ

def User_test():
    user = User()
    Name = "Jožko"
    Last_name = "Hubinský"
    User_Role_id =  db.execute("SELECT id FROM  User_Role ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    user.nahraj(Name,Last_name,User_Role_id)
    assert user.Last_name == Last_name
    assert  user.Name == Name
    assert user.User_Role_id == User_Role_id
    user2 = User().stiahni(user.code)
    Name2 = "Ferko"
    Last_name2 = "Ferkovič"
    user2.Name = Name2
    user2.Last_name = Last_name2
    user2.update()
    user.stiahni(user2.code)
    assert user.Name == Name2
    assert user.Last_name == Last_name2

def Config_test():
    #Insertuje vehicle a customera
    for i in range(20):
        Customer().nahraj("Meno")
        Vehicle().nahraj("POKEMON")

    config = Config()
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    config.nahraj(Customer_id,Vehicle_id)
    assert config.Customer_id == Customer_id
    assert config.Vehicle_id == Vehicle_id
    config2 = Config().stiahni(config.id)
    assert config2.Customer_id == Customer_id
    assert config2.Vehicle_id == Vehicle_id
    Vehicle_id2 = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    config.Vehicle_id = Vehicle_id2
    config.Customer_id = Customer_id2
    config.update()
    assert config.Vehicle_id == Vehicle_id2
    assert config.Customer_id == Customer_id2

def Shipment_test():
    #Insertuje vehicle,Usera a customera
    for i in range(20):
        Customer().nahraj("Meno")
        Vehicle().nahraj("POKEMON")
        user_role_id = db.execute("SELECT id FROM  User_Role ORDER BY RANDOM()").fetchone()[0]
        User().nahraj("Tester","Testovič",user_role_id)
    user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    Date_time_close = str(datetime.datetime(2013, 9, 20,13,00))
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    shipment = Shipment().nahraj(user_code,Date_time_close,Customer_id, Vehicle_id)
    assert shipment.Date_time_close == Date_time_close
    assert shipment.Customer_id == Customer_id
    assert shipment.Vehicle_id == Vehicle_id
    assert shipment.User_code == user_code
    shipment2 = Shipment().stiahni(shipment.id)
    assert shipment2.Date_time_close == Date_time_close
    assert shipment2.id == shipment.id
    assert shipment2.User_code == user_code
    assert shipment2.Vehicle_id == Vehicle_id
    assert shipment2.Customer_id == Customer_id
    user_code2 = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    Date_time_close2 = str(datetime.datetime(2018, 9, 20,13,00))
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    Vehicle_id2 = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    shipment2.User_code = user_code2
    shipment2.Date_time_close = Date_time_close2
    shipment2.Customer_id = Customer_id2
    shipment2.Vehicle_id = Vehicle_id2
    shipment2.update()
    shipment.stiahni(shipment2.id)
    assert shipment.Date_time_close == Date_time_close2
    assert shipment.Customer_id == Customer_id2
    assert shipment.User_code == user_code2
    assert shipment.Vehicle_id == Vehicle_id2

def Pattern_test():
    pattern = Pattern()
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    pattern.nahraj(Customer_id)
    assert pattern.Customer_id == Customer_id
    pattern2 = Pattern().stiahni(pattern.id)
    assert pattern2.Customer_id == pattern.Customer_id
    assert pattern.id == pattern2.id
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    pattern.Customer_id = Customer_id2
    pattern.update()
    pattern2.stiahni(pattern.id)
    assert pattern2.Customer_id == Customer_id2

def Work_statement_test():
    user_code =  db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    work = 5
    time_start = str(datetime.datetime(2013, 9, 20, 13, 00))
    time_end = str(datetime.datetime(2015, 9, 20, 13, 00))
    statement = Work_statement().nahraj(user_code,work,time_start,time_end)
    assert statement.User_code == user_code
    assert statement.Work == work
    assert statement.Time_start == time_start
    assert statement.Time_end == time_end
    statement2 = Work_statement().stiahni(statement.id)
    assert statement2.User_code == user_code
    assert statement2.Work == work
    assert statement2.Time_start == time_start
    assert statement2.Time_end == time_end
    user_code2 =  db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    work2 = 7
    time_start2 = str(datetime.datetime(2018, 9, 20, 13, 00))
    time_end2 = str(datetime.datetime(2019, 9, 20, 13, 00))
    statement.User_code = user_code2
    statement.Work = work2
    statement.Time_start = time_start2
    statement.Time_end = time_end2
    statement.update()
    statement2.stiahni(statement.id)
    assert statement2.User_code == user_code2
    assert statement2.Work == work2
    assert statement2.Time_start == time_start2
    assert statement2.Time_end == time_end2

def Stillage_type_test():
    meno = "Stilidz tajp test"
    type = Stillage_type().nahraj(meno)
    assert meno == type.Name
    type2 = Stillage_type().stiahni(type.id)
    assert meno == type2.Name
    assert type2.id == type.id
    meno2 = "Stilidz tajp test no 2"
    type2.Name = meno2
    type2.update()
    assert meno2 == type2.Name
    type.stiahni(type2.id)
    assert meno2 == type.Name

def Advanced_user_test():
    for i in range(20):
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
        Config().nahraj(Customer_id, Vehicle_id)

    user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    config_id = db.execute("SELECT id FROM  Config ORDER BY RANDOM()").fetchone()[0]
    a_user = Advanced_user().nahraj(config_id,user_code)
    assert a_user.User_code == user_code
    assert a_user.Config_id == config_id
    a_user2 = Advanced_user().stiahni(a_user.id)
    assert a_user.id == a_user2.id
    assert a_user2.User_code == user_code
    assert a_user2.Config_id == config_id
    user_code2 = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    config_id2 = db.execute("SELECT id FROM  Config ORDER BY RANDOM()").fetchone()[0]
    a_user2.User_code = user_code2
    a_user2.Config_id = config_id2
    a_user2.update()
    a_user.stiahni(a_user2.id)
    assert a_user.User_code == user_code2
    assert a_user.Config_id == config_id2

def Stillage_test():
    for i in range(20):
        user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
        Shipment().nahraj(user_code,str(datetime.datetime(2018, 9, 20, 13, 00)), Customer_id,Vehicle_id)
        Stillage_type().nahraj("Test")
    Date_time_start = str(datetime.datetime(2015, 9, 20, 13, 00))
    Date_time_end = str(datetime.datetime(2015, 8, 20, 13, 00))
    Stillage_number = 5
    Stillage_number_on_head = 20
    First_scan_product = 14
    Last_scan_product = 18
    JLR_header = 80
    Carriage_L = "niečo"
    check = 17
    First_scan_TLS = 10222
    Last_scan_TLS = 65222
    stylage_type_id = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    Shipment_id = db.execute("SELECT id FROM  Shipment ORDER BY RANDOM()").fetchone()[0]
    TLS_range_start = 18000
    TLS_range_stop = 185697
    Note = "Noted Note"
    stillage = Stillage().nahraj(Date_time_start, Date_time_end, Stillage_number, Stillage_number_on_head, First_scan_product,
                                 Last_scan_product, JLR_header, Carriage_L,check, First_scan_TLS, Last_scan_TLS,stylage_type_id,Shipment_id, TLS_range_start
                                 , TLS_range_stop, Note)
    assert stillage.Date_time_start == Date_time_start
    assert stillage.Date_time_end == Date_time_end
    assert stillage.Stillage_number == Stillage_number
    assert stillage.Stillage_Number_on_Header == Stillage_number_on_head
    assert stillage.First_scan_product == First_scan_product
    assert stillage.Last_scan_product == Last_scan_product
    assert stillage.JLR_Header_NO == JLR_header
    assert stillage.Carriage_L_JLR_H == Carriage_L
    assert stillage._Check == check
    assert stillage.First_scan_TLS_code == First_scan_TLS
    assert stillage.Last_scan_TLS_code == Last_scan_TLS
    assert stillage.Stillage_Type_id == stylage_type_id
    assert stillage.Shipment_id == Shipment_id
    assert stillage.TLS_range_start == TLS_range_start
    assert stillage.TLS_range_stop == TLS_range_stop
    assert stillage.Note == Note
    stillage2 = Stillage().stiahni(stillage.id)
    assert stillage2.Date_time_start == Date_time_start
    assert stillage2.Date_time_end == Date_time_end
    assert stillage2.Stillage_number == Stillage_number
    assert stillage2.Stillage_Number_on_Header == Stillage_number_on_head
    assert stillage2.First_scan_product == First_scan_product
    assert stillage2.Last_scan_product == Last_scan_product
    assert stillage2.JLR_Header_NO == JLR_header
    assert stillage2.Carriage_L_JLR_H == Carriage_L
    assert stillage2._Check == check
    assert stillage2.First_scan_TLS_code == First_scan_TLS
    assert stillage2.Last_scan_TLS_code == Last_scan_TLS
    assert stillage2.Stillage_Type_id == stylage_type_id
    assert stillage2.Shipment_id == Shipment_id
    assert stillage2.TLS_range_start == TLS_range_start
    assert stillage2.TLS_range_stop == TLS_range_stop
    assert stillage2.Note == Note
    assert stillage2.id == stillage.id
    Date_time_start2 = str(datetime.datetime(2017, 9, 20, 13, 00))
    Date_time_end2 = str(datetime.datetime(2018, 8, 20, 13, 00))
    Stillage_number2 = 52
    Stillage_number_on_head2 = 202
    First_scan_product2 = 142
    Last_scan_product2 = 182
    JLR_header2 = 802
    Carriage_L2 = "niečo 2"
    check2 = 172
    First_scan_TLS2 = 102222
    Last_scan_TLS2 = 652222
    stylage_type_id2 = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    Shipment_id2 = db.execute("SELECT id FROM  Shipment ORDER BY RANDOM()").fetchone()[0]
    TLS_range_start2 = 180002
    TLS_range_stop2 = 1856972
    Note2 = "Noted Note 2"
    stillage2.Date_time_start = Date_time_start2
    stillage2.Date_time_end = Date_time_end2
    stillage2.Stillage_number = Stillage_number2
    stillage2.Stillage_Number_on_Header = Stillage_number_on_head2
    stillage2.First_scan_product = First_scan_product2
    stillage2.Last_scan_product = Last_scan_product2
    stillage2.JLR_Header_NO = JLR_header2
    stillage2.Carriage_L_JLR_H = Carriage_L2
    stillage2._Check = check2
    stillage2.First_scan_TLS_code = First_scan_TLS2
    stillage2.Last_scan_TLS_code = Last_scan_TLS2
    stillage2.Stillage_Type_id = stylage_type_id2
    stillage2.Shipment_id = Shipment_id2
    stillage2.TLS_range_start = TLS_range_start2
    stillage2.TLS_range_stop = TLS_range_stop2
    stillage2.Note = Note2
    stillage2.update()
    stillage.stiahni(stillage2.id)
    assert stillage.Date_time_start == Date_time_start2
    assert stillage.Date_time_end == Date_time_end2
    assert stillage.Stillage_number == Stillage_number2
    assert stillage.Stillage_Number_on_Header == Stillage_number_on_head2
    assert stillage.First_scan_product == First_scan_product2
    assert stillage.Last_scan_product == Last_scan_product2
    assert stillage.JLR_Header_NO == JLR_header2
    assert stillage.Carriage_L_JLR_H == Carriage_L2
    assert stillage._Check == check2
    assert stillage.First_scan_TLS_code == First_scan_TLS2
    assert stillage.Last_scan_TLS_code == Last_scan_TLS2
    assert stillage.Stillage_Type_id == stylage_type_id2
    assert stillage.Shipment_id == Shipment_id2
    assert stillage.TLS_range_start == TLS_range_start2
    assert stillage.TLS_range_stop == TLS_range_stop2
    assert stillage.Note == Note2
    assert stillage.id == stillage2.id

def Pattern_item_test():
    for i in range(20):
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Pattern().nahraj(Customer_id)
    item = Pattern_Item()
    stylage_type_id = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    pattern_id = db.execute("SELECT id FROM  Pattern ORDER BY RANDOM()").fetchone()[0]
    number = 65
    item.nahraj(number,pattern_id,stylage_type_id)
    assert item.Pattern_id == pattern_id
    assert item.Number == number
    assert item.Stillage_type_id ==stylage_type_id
    item2 = Pattern_Item().stiahni(item.id)
    assert item2.Pattern_id == pattern_id
    assert item2.Number == number
    assert item2.Stillage_type_id ==stylage_type_id
    assert item.id == item2.id
    stylage_type_id2 = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    pattern_id2 = db.execute("SELECT id FROM  Pattern ORDER BY RANDOM()").fetchone()[0]
    number2 = 652
    item2.Stillage_type_id = stylage_type_id2
    item2.Pattern_id = pattern_id2
    item2.Number = number2
    item2.update()
    item.stiahni(item2.id)
    assert item.Pattern_id == pattern_id2
    assert item.Number == number2
    assert item.Stillage_type_id ==stylage_type_id2


def last_sync_db_test():
    assert isinstance(parse(db.execute("SELECT last_sync FROM  General ORDER BY RANDOM()").fetchone()[0]),datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  User_Role ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Customer ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  User ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Config ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Shipment ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Pattern ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Work_statement ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Advanced_user ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Stillage ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)
    assert isinstance(parse(db.execute("SELECT last_sync FROM  Pattern_Item ORDER BY RANDOM()").fetchone()[0]),
                      datetime.datetime)


def over_data_general():
    Last_changes = str(datetime.datetime(2013, 9, 20,13,00))
    Last_available = str(datetime.datetime(2015, 10, 22, 13, 00))
    Automatic_export = True
    general = General().nahraj(Last_changes,Last_available,Automatic_export)
    cur.execute(f""" SELECT * from "General" where id = '{general.id}' """)
    k = cur.fetchone()
    #print(k)
    assert str(k[0]) == Last_changes
    assert str(k[1]) == Last_available
    assert k[2] == Automatic_export
    Last_changes2 = str(datetime.datetime(2016, 9, 20,13,00))
    Last_available2 = str(datetime.datetime(2017, 10, 22, 13, 00))
    Automatic_export2 = False
    general.Last_changes = Last_changes2
    general.Last_available = Last_available2
    general.Automatic_export = Automatic_export2
    general.update()
    cur.execute(f""" SELECT * from "General" where id = '{general.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == Last_changes2
    assert str(k[1]) == Last_available2
    assert k[2] == Automatic_export2

def over_data_User_Role():
    meno = "   test   "
    user = User_Role().nahraj(meno)
    cur.execute(f""" SELECT * from "User_Role" where id = '{user.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == meno
    meno2 = " ciprinka  "
    user.name = meno2
    user.update()
    cur.execute(f""" SELECT * from "User_Role" where id = '{user.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == meno2

def over_data_Customer():
    meno = "   test   Customer"
    customer = Customer().nahraj(meno)
    cur.execute(f""" SELECT * from "Customer" where id = '{customer.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == meno
    meno2 = " cipa a.s  "
    customer.Name = meno2
    customer.update()
    cur.execute(f""" SELECT * from "Customer" where id = '{customer.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == meno2

def over_data_Vehicle():
    SPZ = "POKEMON"
    vehicle = Vehicle().nahraj(SPZ)
    cur.execute(f""" SELECT * from "Vehicle" where id = '{vehicle.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == SPZ
    SPZ2 = "KE9842P"
    vehicle.SPZ = SPZ2
    vehicle.update()
    cur.execute(f""" SELECT * from "Vehicle" where id = '{vehicle.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == SPZ2

def over_data_User():
    Name = "Palko"
    Last_name = "Kubický"
    User_Role_id =  db.execute("SELECT id FROM  User_Role ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    user = User().nahraj(Name,Last_name,User_Role_id)
    cur.execute(f""" SELECT * from "User" where code = '{user.code}' """)
    k = cur.fetchone()
    assert k[0] == user.code
    assert k[1] == Name
    assert k[2] == Last_name
    assert k[3] == User_Role_id

    Name2 = "Pavelko"
    Last_name2 = "Práčka"
    User_Role_id2 =  db.execute("SELECT id FROM  User_Role ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    user.Name = Name2
    user.Last_name = Last_name2
    user.User_Role_id = User_Role_id2
    user.update()
    cur.execute(f""" SELECT * from "User" where code = '{user.code}' """)
    k = cur.fetchone()
    assert k[0] == user.code
    assert k[1] == Name2
    assert k[2] == Last_name2
    assert k[3] == User_Role_id2


def over_data_Config():
    for i in range(20):
        Customer().nahraj("Meno")
        Vehicle().nahraj("POKEMON")
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    config = Config().nahraj(Customer_id,Vehicle_id)
    cur.execute(f""" SELECT * from "Config" where id = '{config.id}' """)
    k = cur.fetchone()
    assert k[1] == Customer_id
    assert k[2] == Vehicle_id
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    Vehicle_id2 = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM() LIMIT 1").fetchone()[0]
    config.Customer_id = Customer_id2
    config.Vehicle_id = Vehicle_id2
    config.update()
    cur.execute(f""" SELECT * from "Config" where id = '{config.id}' """)
    k = cur.fetchone()
    assert k[1] == Customer_id2
    assert k[2] == Vehicle_id2

def over_data_Shipment():
    for i in range(20):
        Customer().nahraj("Meno")
        Vehicle().nahraj("POKEMON")
        user_role_id = db.execute("SELECT id FROM  User_Role ORDER BY RANDOM()").fetchone()[0]
        User().nahraj("Tester","Testovič",user_role_id)
    user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    Date_time_close = str(datetime.datetime(2013, 9, 20,13,00))
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    shipment = Shipment().nahraj(user_code,Date_time_close,Customer_id, Vehicle_id)
    cur.execute(f""" SELECT * from "Shipment" where id = '{shipment.id}' """)
    k = cur.fetchone()
    assert k[0] == user_code
    assert str(k[1]) == Date_time_close
    assert k[2] == shipment.id
    assert k[3] == Customer_id
    assert k[4] == Vehicle_id
    user_code2 = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    Date_time_close2 = str(datetime.datetime(2013, 9, 20,13,00))
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    Vehicle_id2 = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
    shipment.User_code = user_code2
    shipment.Date_time_close = Date_time_close2
    shipment.Customer_id = Customer_id2
    shipment.Vehicle_id = Vehicle_id2
    shipment.update()
    cur.execute(f""" SELECT * from "Shipment" where id = '{shipment.id}' """)
    k = cur.fetchone()
    assert k[0] == user_code2
    assert str(k[1]) == Date_time_close2
    assert k[2] == shipment.id
    assert k[3] == Customer_id2
    assert k[4] == Vehicle_id2

def over_data_Pattern():
    Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    pattern = Pattern().nahraj(Customer_id)
    cur.execute(f""" SELECT * from "Pattern" where id = '{pattern.id}' """)
    k = cur.fetchone()
    assert k[0] == pattern.id
    assert k[1] == Customer_id
    Customer_id2 = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
    pattern.Customer_id = Customer_id2
    pattern.update()
    cur.execute(f""" SELECT * from "Pattern" where id = '{pattern.id}' """)
    k = cur.fetchone()
    assert k[0] == pattern.id
    assert k[1] == Customer_id2

def over_data_work_statement():
    user_code =  db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    work = 5
    time_start = str(datetime.datetime(2013, 9, 20, 13, 00))
    time_end = str(datetime.datetime(2015, 9, 20, 13, 00))
    statement = Work_statement().nahraj(user_code,work,time_start,time_end)
    cur.execute(f""" SELECT * from "Work_statement" where id = '{statement.id}' """)
    k = cur.fetchone()
    assert k[0] == user_code
    assert k[1] == work
    assert str(k[2]) == time_start
    assert str(k[3]) == time_end
    assert k[4] == statement.id

    user_code2 =  db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    work2 = 52
    time_start2 = str(datetime.datetime(2113, 9, 20, 13, 00))
    time_end2 = str(datetime.datetime(2115, 9, 20, 13, 00))
    statement.User_code = user_code2
    statement.Work = work2
    statement.Time_start = time_start2
    statement.Time_end = time_end2
    statement.update()
    cur.execute(f""" SELECT * from "Work_statement" where id = '{statement.id}' """)
    k = cur.fetchone()
    assert k[0] == user_code2
    assert k[1] == work2
    assert str(k[2]) == time_start2
    assert str(k[3]) == time_end2
    assert k[4] == statement.id

def over_data_stillage_type():
    meno = "Stilidz tajp test"
    type = Stillage_type().nahraj(meno)
    cur.execute(f""" SELECT * from "Stillage_type" where id = '{type.id}' """)
    k = cur.fetchone()
    assert k[0] == meno
    assert k[1] == type.id
    meno2 = "Stilidz tajp test 2 "
    type.Name = meno2
    type.update()
    cur.execute(f""" SELECT * from "Stillage_type" where id = '{type.id}' """)
    k = cur.fetchone()
    assert k[0] == meno2
    assert k[1] == type.id

def over_data_advanced_user():
    for i in range(20):
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
        Config().nahraj(Customer_id, Vehicle_id)

    user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    config_id = db.execute("SELECT id FROM  Config ORDER BY RANDOM()").fetchone()[0]
    a_user = Advanced_user().nahraj(config_id, user_code)
    cur.execute(f""" SELECT * from "Advanced_user" where id = '{a_user.id}' """)
    k = cur.fetchone()
    assert k[0] == a_user.id
    assert k[1] == config_id
    assert k[2] == user_code

    user_code2 = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
    config_id2 = db.execute("SELECT id FROM  Config ORDER BY RANDOM()").fetchone()[0]
    a_user.User_code = user_code2
    a_user.Config_id = config_id2
    a_user.update()
    cur.execute(f""" SELECT * from "Advanced_user" where id = '{a_user.id}' """)
    k = cur.fetchone()
    assert k[0] == a_user.id
    assert k[1] == config_id2
    assert k[2] == user_code2

def over_data_Stillage():
    for i in range(20):
        user_code = db.execute("SELECT code FROM  User ORDER BY RANDOM()").fetchone()[0]
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Vehicle_id = db.execute("SELECT id FROM  Vehicle ORDER BY RANDOM()").fetchone()[0]
        Shipment().nahraj(user_code,str(datetime.datetime(2018, 9, 20, 13, 00)), Customer_id,Vehicle_id)
        Stillage_type().nahraj("Test")
    Date_time_start = str(datetime.datetime(2017, 9, 20, 13, 00))
    Date_time_end = str(datetime.datetime(2018, 8, 20, 13, 00))
    Stillage_number = 5
    Stillage_number_on_head = 20
    First_scan_product = 14
    Last_scan_product = 18
    JLR_header = 80
    Carriage_L = "niečo"
    check = 17
    First_scan_TLS = 10222
    Last_scan_TLS = 65222
    stylage_type_id = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    Shipment_id = db.execute("SELECT id FROM  Shipment ORDER BY RANDOM()").fetchone()[0]
    TLS_range_start = 18000
    TLS_range_stop = 185697
    Note = "Noted Note"
    stillage = Stillage().nahraj(Date_time_start, Date_time_end, Stillage_number, Stillage_number_on_head, First_scan_product,
                                 Last_scan_product, JLR_header, Carriage_L,check, First_scan_TLS, Last_scan_TLS,stylage_type_id,Shipment_id, TLS_range_start
                                 , TLS_range_stop, Note)
    cur.execute(f""" SELECT * from "Stillage" where id = '{stillage.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == Date_time_start
    assert str(k[1]) == Date_time_end
    assert k[2] == Stillage_number
    assert k[3] == Stillage_number_on_head
    assert k[4] == First_scan_product
    assert k[5] == Last_scan_product
    assert k[6] == JLR_header
    assert k[7] == Carriage_L
    assert k[8] == check
    assert k[9] == First_scan_TLS
    assert k[10] == Last_scan_TLS
    assert k[11] == stillage.id
    assert k[12] == stylage_type_id
    assert k[13] == Shipment_id
    assert k[14] == TLS_range_start
    assert k[15] == TLS_range_stop
    assert k[16] == Note

    Date_time_start2 = str(datetime.datetime(2027, 9, 20, 13, 00))
    Date_time_end2 = str(datetime.datetime(2038, 8, 20, 13, 00))
    Stillage_number2 = 54
    Stillage_number_on_head2 = 203
    First_scan_product2 = 149
    Last_scan_product2 = 187
    JLR_header2 = 808
    Carriage_L2 = "niečo naniečo"
    check2 = 178
    First_scan_TLS2 = 102227
    Last_scan_TLS2 = 652224
    stylage_type_id2 = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    Shipment_id2 = db.execute("SELECT id FROM  Shipment ORDER BY RANDOM()").fetchone()[0]
    TLS_range_start2 = 180004
    TLS_range_stop2 = 18569725
    Note2 = "Noted Note Noted"
    stillage.Date_time_start = Date_time_start2
    stillage.Date_time_end = Date_time_end2
    stillage.Stillage_number = Stillage_number2
    stillage.Stillage_Number_on_Header = Stillage_number_on_head2
    stillage.First_scan_product = First_scan_product2
    stillage.Last_scan_product = Last_scan_product2
    stillage.JLR_Header_NO = JLR_header2
    stillage.Carriage_L_JLR_H = Carriage_L2
    stillage._Check = check2
    stillage.First_scan_TLS_code = First_scan_TLS2
    stillage.Last_scan_TLS_code = Last_scan_TLS2
    stillage.Stillage_Type_id = stylage_type_id2
    stillage.Shipment_id = Shipment_id2
    stillage.TLS_range_start = TLS_range_start2
    stillage.TLS_range_stop = TLS_range_stop2
    stillage.Note = Note2
    stillage.update()
    cur.execute(f""" SELECT * from "Stillage" where id = '{stillage.id}' """)
    k = cur.fetchone()
    assert str(k[0]) == Date_time_start2
    assert str(k[1]) == Date_time_end2
    assert k[2] == Stillage_number2
    assert k[3] == Stillage_number_on_head2
    assert k[4] == First_scan_product2
    assert k[5] == Last_scan_product2
    assert k[6] == JLR_header2
    assert k[7] == Carriage_L2
    assert k[8] == check2
    assert k[9] == First_scan_TLS2
    assert k[10] == Last_scan_TLS2
    assert k[11] == stillage.id
    assert k[12] == stylage_type_id2
    assert k[13] == Shipment_id2
    assert k[14] == TLS_range_start2
    assert k[15] == TLS_range_stop2
    assert k[16] == Note2

def over_data_Pattern_Item():
    for i in range(20):
        Customer_id = db.execute("SELECT id FROM  Customer ORDER BY RANDOM()").fetchone()[0]
        Pattern().nahraj(Customer_id)
    item = Pattern_Item()
    stylage_type_id = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    pattern_id = db.execute("SELECT id FROM  Pattern ORDER BY RANDOM()").fetchone()[0]
    number = 65
    item.nahraj(number,pattern_id,stylage_type_id)
    cur.execute(f""" SELECT * from "Pattern_Item" where id = '{item.id}' """)
    k = cur.fetchone()
    assert k[0] == number
    assert k[1] == item.id
    assert k[2] == pattern_id
    assert k[3] == stylage_type_id
    stylage_type_id2 = db.execute("SELECT id FROM  Stillage_type ORDER BY RANDOM()").fetchone()[0]
    pattern_id2 = db.execute("SELECT id FROM  Pattern ORDER BY RANDOM()").fetchone()[0]
    number2 = 652
    item.Stillage_type_id = stylage_type_id2
    item.Pattern_id = pattern_id2
    item.Number = number2
    item.update()
    cur.execute(f""" SELECT * from "Pattern_Item" where id = '{item.id}' """)
    k = cur.fetchone()
    assert k[0] == number2
    assert k[1] == item.id
    assert k[2] == pattern_id2
    assert k[3] == stylage_type_id2

def test_vrat_vsetky():
    general_pocet = db.execute("SELECT COUNT(*) FROM GENERAL").fetchone()[0]
    #print(general_pocet)
    general_vrat_vsetky_klasa = General().vrat_vsetky(True)
    assert len(general_vrat_vsetky_klasa) == general_pocet
    if None in general_vrat_vsetky_klasa: assert False
    assert len(General().vrat_vsetky()) == general_pocet

    pocet = db.execute("SELECT COUNT(*) FROM User_Role").fetchone()[0]
    klasa = User_Role()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Customer").fetchone()[0]
    klasa = Customer()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Vehicle").fetchone()[0]
    klasa = Vehicle()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM User").fetchone()[0]
    klasa = User()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Config").fetchone()[0]
    klasa = Config()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Shipment").fetchone()[0]
    klasa = Shipment()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Pattern").fetchone()[0]
    klasa = Pattern()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Work_statement").fetchone()[0]
    klasa = Work_statement()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Stillage_type").fetchone()[0]
    klasa = Stillage_type()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Advanced_user").fetchone()[0]
    klasa = Advanced_user()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Stillage").fetchone()[0]
    klasa = Stillage()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

    pocet = db.execute("SELECT COUNT(*) FROM Pattern_Item").fetchone()[0]
    klasa = Pattern_Item()
    #print(pocet)
    vrat_vsetky_klasa = klasa.vrat_vsetky(True)
    assert len(vrat_vsetky_klasa) == pocet
    if None in vrat_vsetky_klasa: assert False
    assert len(klasa.vrat_vsetky()) == pocet

def over_synchronizacia():
    vyprazdni_db()
    synchronize_db_server_client()
    for tabulka in tabulky:
        cur.execute(f""" SELECT COUNT(*) FROM "{tabulka}" """)
        assert cur.fetchone()[0] == db.execute(f""" SELECT COUNT(*) FROM {tabulka} """).fetchone()[0]




if __name__ == '__main__':
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall())
    start_time = time.time()
    #Test obsahu tried
    vyprazdni_db()
    General_test()
    User_role_test()
    Customer_test()
    Vehicle_test()
    User_test()
    Config_test()
    Shipment_test()
    Pattern_test()
    Work_statement_test()
    Stillage_type_test()
    Advanced_user_test()
    Stillage_test()
    Pattern_item_test()
    test_vrat_vsetky()
    print("TEST OBSAHU A ŠTRUKTÚRY TRIED OK - trval %s sekúnd" % (time.time() - start_time))
    #Test obsahu vzdialenej databázy
    start_time = time.time()
    last_sync_db_test()
    over_data_general()
    over_data_User_Role()
    over_data_Customer()
    over_data_Vehicle()
    over_data_User()
    over_data_Config()
    over_data_Shipment()
    over_data_Pattern()
    over_data_work_statement()
    over_data_stillage_type()
    over_data_advanced_user()
    over_data_Stillage()
    over_data_Pattern_Item()
    over_synchronizacia()
    vyprazdni_db()
    print("TEST OBSAHU DB OK - trval %s sekúnd" % (time.time() - start_time))