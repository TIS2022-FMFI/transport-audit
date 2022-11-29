from sqlite import *
#Pred testom sa uisti, že máš najnovšiu verziu štruktúry databázy z githubu (gefco.db)
#!!!!!!!!!!!!!!!!
# Všetky dáta z lokálnej databázy budú zmazané
#!!!!!!!!!!!!!!!

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



if __name__ == '__main__':
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall())
    start_time = time.time()

    vyprazdni_db()
    General_test()
    User_role_test()
    Customer_test()
    Vehicle_test()
    User_test()
    print("TEST OK - trval %s sekúnd" % (time.time() - start_time))