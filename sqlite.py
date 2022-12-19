import json
import uuid
import time
import sqlite3
import requests
import datetime
import random
#pip install python-dateutil
from dateutil.parser import parse
import os
from config import allow_synchronize,sync_URL,api_password
db_path = os.path.abspath(os.path.dirname(__file__)) + "/gefco.db"
db_path = os.path.normpath(db_path)
#print(db_path)
db = sqlite3.connect(db_path)
cursor = db.cursor()
tabulky = ["General", "User_Role", "Customer", "Vehicle", "User", "Config", "Shipment", "Pattern", "Work_statement","Stillage_type", "Advanced_user", "Stillage", "Pattern_Item"]  # Vsetky tabulky

MAZACIA_KONSTANTA = "DELETED" #Doplnok obsahujuci tento text sa povazuje za zmazany

def overit_zmazanie(tabulka,id):
    if tabulka == "User":
        cursor.execute(f"SELECT * FROM {tabulka} WHERE code=?", [id])  #
    else:
        cursor.execute(f"SELECT * FROM {tabulka} WHERE id=?", [id])  #
    col_name = [i[0] for i in cursor.description]
    test = cursor.fetchone()
    if test is None:
        return None
    data = dict(zip(col_name, test))
    if data['doplnok'] == MAZACIA_KONSTANTA:
        return True
    if data['doplnok'] == "" or data['doplnok']==None:
        return False
    return data['doplnok']

def zmaz_zaznam(tabulka,id,ine = MAZACIA_KONSTANTA):
    # dorobit kod pre User
    if tabulka == "User":
        cursor.execute(f"SELECT * FROM {tabulka} WHERE code=?", [id])  #
    else:
        cursor.execute(f"SELECT * FROM {tabulka} WHERE id=?", [id])  #
    col_name = [i[0] for i in cursor.description]
    test = cursor.fetchone()
    if test is None:
        return None
    data = dict(zip(col_name, test))
    if(data['doplnok'] == ine):
        return False
    if tabulka == "User":
        db.execute(f"UPDATE {tabulka} set doplnok = '{ine}', last_sync = '{str(datetime.datetime.now())}' WHERE code = {id}")
    else:
        db.execute(f"UPDATE {tabulka} set doplnok = '{ine}', last_sync = '{str(datetime.datetime.now())}' WHERE id = '{id}'")
    data['doplnok'] = ine
    data['last_sync'] = str(parse(str(datetime.datetime.now())))
    cursor.execute("COMMIT")
    try:
        client_server_nahraj_jeden(tabulka, data)  #
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return True

def overit_vykonavatela(tabulka,id):
    if tabulka == "User":
        cursor.execute(f"SELECT * FROM {tabulka} WHERE code=?", [id])  #
    else:
        cursor.execute(f"SELECT * FROM {tabulka} WHERE id=?", [id])  #
    col_name = [i[0] for i in cursor.description]
    test = cursor.fetchone()
    if test is None:
        return None
    data = dict(zip(col_name, test))
    if data['vykonavatel'] == None:
        return None
    return data['vykonavatel']

def vloz_vykonavatela(tabulka,id,ine = None):
    if tabulka == "User":
        cursor.execute(f"SELECT * FROM {tabulka} WHERE code=?", [id])  #
    else:
        cursor.execute(f"SELECT * FROM {tabulka} WHERE id=?", [id])  #
    col_name = [i[0] for i in cursor.description]
    test = cursor.fetchone()
    if test is None:
        return None
    data = dict(zip(col_name, test))
    if(data['vykonavatel'] == ine):
        return False
    if tabulka == "User":
        db.execute(f"UPDATE {tabulka} set vykonavatel = {ine}, last_sync = '{str(datetime.datetime.now())}' WHERE code = {id}")
    else:
        db.execute(f"UPDATE {tabulka} set vykonavatel = {ine}, last_sync = '{str(datetime.datetime.now())}' WHERE id = '{id}'")
    data['vykonavatel'] = ine
    data['last_sync'] = str(parse(str(datetime.datetime.now())))
    cursor.execute("COMMIT")
    try:
        client_server_nahraj_jeden(tabulka, data)  #
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return True


def all_user_codes():
    cursor.execute("SELECT code FROM User")
    vysledok = set()
    for i in cursor.fetchall():
        vysledok.add(i[0])
    return vysledok


def synchronize_db_server_client():
    if(allow_synchronize==False): return False
    for nazov_tabulky in tabulky:
        URL = f"{sync_URL}/Get"
        post = {
            "api-heslo": f"{api_password}",
            "tabulka": f"{nazov_tabulky}"
        }
        r = requests.post(url=URL, json=post,timeout=None)
        data = r.json()
        cursor.execute("begin")
        for i in data:
            #Zacinam kontrolu, či sa zaznam nachadza už v lokalnej db
            if(nazov_tabulky=="User"):
                over_uuid = """SELECT EXISTS(SELECT 1 FROM %s WHERE code = '%s')""" % (nazov_tabulky,i.get("code"))
                over_timestamp = """SELECT last_sync FROM %s WHERE code = '%s'""" % (nazov_tabulky,i.get("code"))
                pozor_vymazanie = """DELETE FROM %s WHERE code = '%s'""" % (nazov_tabulky, i.get("code"))
            else:
                over_uuid = """SELECT EXISTS(SELECT 1 FROM %s WHERE id = '%s')""" % (nazov_tabulky,i.get("id"))
                over_timestamp = """SELECT last_sync FROM %s WHERE id = '%s'""" % (nazov_tabulky, i.get("id"))
                pozor_vymazanie = """DELETE FROM %s WHERE id = '%s'""" % (nazov_tabulky, i.get("id"))
            cursor.execute(over_uuid)
            #nachadza sa, overujem timestamp, inak skipujem
            if cursor.fetchone() == (1,):
                cursor.execute(over_timestamp)
                lokalny_timestamp = parse(cursor.fetchone()[0])
                server_timestamp = parse(i.get("last_sync"))
                if server_timestamp > lokalny_timestamp:
                    cursor.execute(pozor_vymazanie)
                    #print("mazem")
                else:
                    continue
            # Tu uz zacina vkladanie hodnot
            #Mazem vsetky hodnoty, obsahujuce none, pretože sqlite tabulky maju nejake nezmyselne struktury. Co ma byt none sa aj tak doplni db samo
            filtrovane = {k: v for k, v in i.items() if v is not None}

            columns = ', '.join(filtrovane.keys())
            placeholders = ':' + ', :'.join(filtrovane.keys())
            query = """INSERT INTO %s (%s) VALUES (%s)""" % (nazov_tabulky, columns, placeholders)
            cursor.execute(query, filtrovane)
        cursor.execute("COMMIT")

#dorobit synchronizáciu lokál --> server
def synchronize_db_client_server():
    if (allow_synchronize == False): return False
    vysledky_rekvestov = []
    for nazov_tabulky in tabulky:
        cursor.execute("""SELECT * FROM %s""" % (nazov_tabulky))
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        #print(nazov_tabulky,temp)
        URL = f"{sync_URL}/Post"
        post = {
            "api-heslo": f"{api_password}",
            "tabulka": f"{nazov_tabulky}",
            "data" : vysledok
        }
        r = requests.post(url=URL, json=post, timeout=None)
        #print(f"Nahrávam {nazov_tabulky}")
        vysledky_rekvestov.append(r) #Aby som nesiel príliš rýchlo, potom sa nestihnú tabulky spracovat v spravnom poradí a to vedie k zlým foreign keys
    return vysledky_rekvestov
def client_server_nahraj_jeden(nazov_tabulky,data):
    if (allow_synchronize == False): return False
    vysledok = [data]
    URL = f"{sync_URL}/Post"
    post = {
        "api-heslo": f"{api_password}",
        "tabulka": f"{nazov_tabulky}",
        "data" : vysledok
    }
    r = requests.post(url=URL, json=post, timeout=None)
    return r.text

#Tu zacinaju tabulky ako classy --------------------------------------------------------------------------------------------------------------------
class Customer:
    __tablename__ = "Customer"
    def __init__(self):
        self.Name = None
        self.id = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)

    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Customer")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Customer().stiahni(riadok[1]))
            return vysledok
        cursor.execute("Select * from Customer")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Customer WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Name = data['Name']
        self.id = data['id']
        return self
    def nahraj(self,Name): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Name = Name
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Customer WHERE (id=?)', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Customer (id, Name) VALUES (?,?)', (self.id, self.Name))#
            cursor.execute("COMMIT")
            data = dict()
            data['id'] = self.id
            data['Name'] = self.Name
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Customer",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE CUSTOMER SET Name= '%s', last_sync = '%s' WHERE id = '%s'""" % (self.Name,parse(str(datetime.datetime.now())),self.id)
            cursor.execute(sql)
            cursor.execute("COMMIT")
            data = dict()
            data['id'] = self.id
            data['Name'] = self.Name
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Customer",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None



class General():
    __tablename__ = "General"
    def __int__(self):
        self.Last_changes = None
        self.Last_available = None
        self.Automatic_export = None
        self.id = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self,klasy = False): # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from General")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(General().stiahni(riadok[3]))
            return vysledok
        cursor.execute("Select * from General")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM General WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Last_changes = data['Last_changes']
        self.Last_available = data['Last_available']
        self.Automatic_export = data['Automatic_export']
        self.id = data['id']
        return self
    def nahraj(self,Last_changes,Last_available,Automatic_export): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Last_changes = Last_changes
        self.Last_available = Last_available
        self.Automatic_export = Automatic_export
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM General WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO General (id, Last_changes, Last_available, Automatic_export) VALUES (?,?,?,?)', (self.id, self.Last_changes,self.Last_available,self.Automatic_export))#
            cursor.execute("COMMIT")
            data = dict()
            data['Last_changes'] = str(self.Last_changes)
            data['Last_available'] = str(self.Last_available)
            data['Automatic_export'] = self.Automatic_export
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("General",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE General SET Last_changes= ?,Last_available=?,Automatic_export = ?, last_sync= ? WHERE id = ?"""
            cursor.execute(sql,(self.Last_changes,self.Last_available,self.Automatic_export,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Last_changes'] = str(self.Last_changes)
            data['Last_available'] = str(self.Last_available)
            data['Automatic_export'] = self.Automatic_export
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("General",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class Stillage_type():
    __tablename__ = "Stillage_type"
    def __int__(self):
        self.Name = None
        self.id = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)



    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Stillage_type")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Stillage_type().stiahni(riadok[1]))
            return vysledok
        cursor.execute("Select * from Stillage_type")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Stillage_type WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Name = data['Name']
        self.id = data['id']
        return self

    def stiahniMeno(self,meno): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Stillage_type WHERE Name=?", [meno])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchall()
        for r in test:
            data = dict(zip(col_name, test))
            if data['doplnok'] != 'DELETED':
                self.Name = data['Name']
                self.id = data['id']
                return self
        return
    def nahraj(self,Name): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Name = Name
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Stillage_type WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Stillage_type (id, Name) VALUES (?,?)', (self.id, self.Name))#
            cursor.execute("COMMIT")
            data = dict()
            data['Name'] = self.Name
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Stillage_type",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE Stillage_type SET Name = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql,(self.Name,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Name'] = self.Name
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Stillage_type",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class User_Role():
    __tablename__ = "User_Role"
    def __init__(self):
        self.name = None
        self.id = None


    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)

    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from User_Role")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(User_Role().stiahni(riadok[1]))
            return vysledok
        cursor.execute("Select * from User_Role")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM User_Role WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.name = data['name']
        self.id = data['id']
        return self
    def nahraj(self,name): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.name = name
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM User_Role WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO User_Role (id, name) VALUES (?,?)', (self.id, self.name))#
            cursor.execute("COMMIT")
            data = dict()
            data['name'] = self.name
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("User_Role",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE User_Role SET name = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql,(self.name,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['name'] = self.name
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("User_Role",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class Vehicle():
    __tablename__ = "Vehicle"
    def __init__(self):
     self.SPZ = None
     self.id = None
     self.Name = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Vehicle")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Vehicle().stiahni(riadok[1]))
            return vysledok
        cursor.execute("Select * from Vehicle")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Vehicle WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.SPZ = data['SPZ']
        self.id = data['id']
        self.Name = self.SPZ
        return self
    def nahraj(self,SPZ): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.SPZ = SPZ
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Vehicle WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Vehicle (id, SPZ) VALUES (?,?)', (self.id, self.SPZ))#
            cursor.execute("COMMIT")
            data = dict()
            data['SPZ'] = self.SPZ
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Vehicle",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE Vehicle SET SPZ = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql,(self.SPZ,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['SPZ'] = self.SPZ
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Vehicle",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class Config():
    __tablename__ = "Config"
    def __init__(self):
        self.id = None
        self.Customer_id = None
        self.Vehicle_id = None

    def edit_configs(self):
        cursor.execute(
            "select * from Customer C inner join Config C2 on C.id = C2.Customer_id inner join Vehicle V on V.id = C2.Vehicle_id where C.doplnok isnull and C2.doplnok isnull and V.doplnok isnull;")
        data = []
        for i in cursor.fetchall():
            data.append(i)
        return data

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Config")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Config().stiahni(riadok[0]))
            return vysledok
        cursor.execute("Select * from Config")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok

    def configyZakaznika(self, idZakaznika):
        cursor.execute("Select * from Config WHERE Customer_id=?", [idZakaznika])  #
        vysledok = []
        col_name = [i[0] for i in cursor.description]
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            if temp['doplnok'] != 'DELETED':
                vysledok.append(Config().stiahni(riadok[0]))
        return vysledok

    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Config WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Customer_id = data['Customer_id']
        self.Vehicle_id = data['Vehicle_id']
        self.id = data['id']
        return self
    def nahraj(self,Customer_id,Vehicle_id): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Customer_id = Customer_id
        self.Vehicle_id = Vehicle_id
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Config WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Config (id, Customer_id, Vehicle_id) VALUES (?,?,?)', (self.id, self.Customer_id, self.Vehicle_id))#
            cursor.execute("COMMIT")
            data = dict()
            data['Customer_id'] = self.Customer_id
            data['Vehicle_id'] = self.Vehicle_id
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Config",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE Config SET Customer_id = ?, Vehicle_id = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql,(self.Customer_id,self.Vehicle_id,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Customer_id'] = self.Customer_id
            data['Vehicle_id'] = self.Vehicle_id
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Config",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None

class Pattern():
    __tablename__ = "Pattern"
    def __init__(self):
        self.id = None
        self.Customer_id = None

    def Data_on_editing(self):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute(
            "select * from Customer c inner join Pattern P on c.id = P.Customer_id inner join Pattern_Item PI on P.id = PI.Pattern_id inner join Stillage_type St on St.id = PI.Stillage_type_id where c.doplnok isnull and P.doplnok isnull and PI.doplnok isnull and St.doplnok isnull;")

        data = []
        for i in cursor.fetchall():
            data.append(i)
        return data


    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)

    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Pattern")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Pattern().stiahni(riadok[0]))
            return vysledok
        cursor.execute("Select * from Pattern")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Pattern WHERE id=?", [id])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Customer_id = data['Customer_id']
        self.id = data['id']
        return self

    def zozbieraneUdajePatternu(self, id):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute(
            "SELECT * from Customer c JOIN Pattern P on c.id = P.Customer_id JOIN Pattern_Item PI on P.id = PI.Pattern_id JOIN Stillage_type St on St.id = PI.Stillage_type_id WHERE c.id=?", [id])

        data = []
        for i in cursor.fetchall():
            data.append(i)
        return data

    def patternZakaznika(self,id): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Pattern WHERE Customer_id=? ", [id])#
        col_name = [i[0] for i in cursor.description]

        for riadok in cursor.fetchall():
            data = dict(zip(col_name, riadok))
            if data['doplnok'] != 'DELETED':
                return Pattern().stiahni(riadok[0])
        return None


    def nahraj(self,Customer_id): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Customer_id = Customer_id
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Pattern WHERE id = ?', [self.id])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Pattern (id, Customer_id) VALUES (?,?)', (self.id, self.Customer_id))#
            cursor.execute("COMMIT")
            data = dict()
            data['Customer_id'] = self.Customer_id
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Pattern",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.id:
            sql = """UPDATE Pattern SET Customer_id = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql,(self.Customer_id,parse(str(datetime.datetime.now())),self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Customer_id'] = self.Customer_id
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Pattern",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None

class User():
    __tablename__ = "User"
    def __init__(self):
        self.code = None
        self.Name = None
        self.Last_name = None
        self.User_Role_id = None

    def over_zmazanie(self):
        if(self.code ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.code)
        return over

    def zmazat(self,doplnok = ""):
        if (self.code == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.code)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.code,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.code == None: return None
        return overit_vykonavatela(self.__tablename__,self.code)
    def nastav_vykonavatela(self,kod):
        if self.code == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.code,kod)

    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from User")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(User().stiahni(riadok[0]))
            return vysledok
        cursor.execute("Select * from User")#
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok
    def stiahni(self,code): #Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM User WHERE code=?", [code])#
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Name = data['Name']
        self.Last_name = data['Last_name']
        self.User_Role_id = data['User_Role_id']
        self.code = data['code']
        return self
    def nahraj(self,Name,Last_name,User_Role_id): #Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Name = Name
        self.Last_name = Last_name
        self.User_Role_id = User_Role_id
        #Generovanie user kodu, aký ešte nieje v db
        while True: # celý tento vtip je úplne zbytočný, skôr vyhrám v športke ako to, že trafím 2x 15 miestne user kódy
            random_code = random.Random().randint(10001,99999) # náhodný 5 miestny int
            if(random_code in all_user_codes()):
                pass
            else:
                self.code = random_code
                break
        cursor.execute('SELECT * FROM User WHERE code = ?', [self.code])#
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO User (code, Name, Last_name, User_Role_id) VALUES (?,?,?,?)', (self.code, self.Name,self.Last_name,self.User_Role_id))#
            cursor.execute("COMMIT")
            data = dict()
            data['Name'] = self.Name
            data['Last_name'] = self.Last_name
            data['User_Role_id'] = self.User_Role_id
            data['code'] = self.code
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("User",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None
    def update(self):
        if self.code:
            sql = """UPDATE User SET Name = ?, Last_name = ?, User_Role_id = ?, last_sync = ? WHERE code = ?"""
            cursor.execute(sql,(self.Name,self.Last_name,self.User_Role_id,parse(str(datetime.datetime.now())),self.code))
            cursor.execute("COMMIT")
            data = dict()
            data['Name'] = self.Name
            data['Last_name'] = self.Last_name
            data['User_Role_id'] = self.User_Role_id
            data['code'] = self.code
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("User",data)#
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class Advanced_user():
     __tablename__ = "Advanced_user"
     def __init__(self):
        self.id = None
        self.Config_id = None
        self.User_code = None

     def over_zmazanie(self):
         if (self.id == None):
             return None
         over = overit_zmazanie(self.__tablename__, self.id)
         return over

     def zmazat(self, doplnok=""):
         if (self.id == None):
             return None
         if doplnok == "":
             zmaz = zmaz_zaznam(self.__tablename__, self.id)
         else:
             zmaz = zmaz_zaznam(self.__tablename__, self.id, doplnok)
         return zmaz

     def vrat_vykonavatela(self):
         if self.id == None: return None
         return overit_vykonavatela(self.__tablename__, self.id)

     def nastav_vykonavatela(self, kod):
         if self.id == None or kod == None or isinstance(kod, int) == False:
             return None
         return vloz_vykonavatela(self.__tablename__, self.id, kod)

     def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
         if klasy:
             cursor.execute("Select * from Advanced_user")  #
             vysledok = []
             for riadok in cursor.fetchall():
                 vysledok.append(Advanced_user().stiahni(riadok[0]))
             return vysledok
         cursor.execute("Select * from Advanced_user")  #
         col_name = [i[0] for i in cursor.description]
         vysledok = []
         for riadok in cursor.fetchall():
             temp = dict(zip(col_name, riadok))
             vysledok.append(temp)
         return vysledok

     def stiahni(self, id):  # Vráti None ak neexistuje, inak vráti class
         cursor.execute("SELECT * FROM Advanced_user WHERE id=?", [id])  #
         col_name = [i[0] for i in cursor.description]
         test = cursor.fetchone()
         if test is None:
             return None
         data = dict(zip(col_name, test))
         self.Config_id = data['Config_id']
         self.User_code = data['User_code']
         self.id = data['id']
         return self

     def nahraj(self, Config_id,User_code):  # Ak záznam existuje vráti None, inak ho nahra do db a vrati class
         self.Config_id = Config_id
         self.User_code = User_code
         self.id = str(uuid.uuid4())
         cursor.execute('SELECT * FROM Advanced_user WHERE id = ?', [self.id])  #
         entry = cursor.fetchone()
         if entry is None:
             cursor.execute('INSERT INTO Advanced_user (id, Config_id, User_code) VALUES (?,?,?)', (self.id, self.Config_id,self.User_code))  #
             cursor.execute("COMMIT")
             data = dict()
             data['Config_id'] = self.Config_id
             data['User_code'] = self.User_code
             data['id'] = self.id
             data['last_sync'] = str(parse(str(datetime.datetime.now())))
             try:
                 client_server_nahraj_jeden("Advanced_user", data)  #
             except requests.exceptions.HTTPError as errh:
                 print("Http Error:", errh)
             except requests.exceptions.ConnectionError as errc:
                 print("Error Connecting:", errc)
             except requests.exceptions.Timeout as errt:
                 print("Timeout Error:", errt)
             except requests.exceptions.RequestException as err:
                 print("OOps: Something Else", err)
             return self
         else:
             return None

     def update(self):
         if self.id:
             sql = """UPDATE Advanced_user SET Config_id = ?, User_code = ?, last_sync = ? WHERE id = ?"""
             cursor.execute(sql, (self.Config_id,self.User_code, parse(str(datetime.datetime.now())), self.id))
             cursor.execute("COMMIT")
             data = dict()
             data['Config_id'] = self.Config_id
             data['id'] = self.id
             data['User_code'] = self.User_code
             data['last_sync'] = str(parse(str(datetime.datetime.now())))
             try:
                 client_server_nahraj_jeden("Advanced_user", data)  #
             except requests.exceptions.HTTPError as errh:
                 print("Http Error:", errh)
             except requests.exceptions.ConnectionError as errc:
                 print("Error Connecting:", errc)
             except requests.exceptions.Timeout as errt:
                 print("Timeout Error:", errt)
             except requests.exceptions.RequestException as err:
                 print("OOps: Something Else", err)
             return self
         return None


class Pattern_Item():
    __tablename__ = "Pattern_Item"
    def __init__(self):
     self.Number = None
     self.id = None
     self.Pattern_id = None
     self.Stillage_type_id = None


    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Pattern_Item")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Pattern_Item().stiahni(riadok[1]))
            return vysledok
        cursor.execute("Select * from Pattern_Item")  #
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok

    def stiahni(self, id):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Pattern_Item WHERE id=?", [id])  #
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Pattern_id = data['Pattern_id']
        self.Stillage_type_id = data['Stillage_type_id']
        self.Number = data['Number']
        self.id = data['id']
        return self

    def vrat_vsetkyPattern(self, idPatternu):  # Vypíše všetky riadky, vráti ako dictionary
        cursor.execute("Select * from Pattern_Item WHERE Pattern_id=?", [idPatternu])  #
        vysledok = []
        for riadok in cursor.fetchall():
            r = Pattern_Item()
            r.Number = riadok[0]
            r.id = riadok[1]
            r.Pattern_id = riadok[2]
            r.Stillage_type_id = riadok[3]
            if not r.over_zmazanie():
                vysledok.append(r)

        #['Number', 'id', 'Pattern_id', 'Stillage_type_id', 'last_sync', 'doplnok', 'vykonavatel']

        return vysledok


    def nahraj(self, Number, Pattern_id,Stillage_type_id):  # Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Number = Number
        self.Pattern_id = Pattern_id
        self.Stillage_type_id = Stillage_type_id
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Pattern_Item WHERE id = ?', [self.id])  #
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Pattern_Item (id, Number, Pattern_id, Stillage_type_id) VALUES (?,?,?,?)',
                           (self.id, self.Number, self.Pattern_id, self.Stillage_type_id))  #
            cursor.execute("COMMIT")
            data = dict()
            data['Number'] = self.Number
            data['Pattern_id'] = self.Pattern_id
            data['Stillage_type_id'] = self.Stillage_type_id
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Pattern_Item", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None

    def update(self):
        if self.id:
            sql = """UPDATE Pattern_Item SET Number = ?, Pattern_id = ?, Stillage_type_id = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql, (self.Number, self.Pattern_id,self.Stillage_type_id, parse(str(datetime.datetime.now())), self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Number'] = self.Number
            data['id'] = self.id
            data['Pattern_id'] = self.Pattern_id
            data['Stillage_type_id'] = self.Stillage_type_id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Pattern_Item", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None


class Shipment():
    __tablename__ = "Shipment"
    def __init__(self):
        self.User_code = None
        self.Date_time_close = None
        self.id = None
        self.Customer_id = None
        self.Vehicle_id = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Shipment")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Shipment().stiahni(riadok[2]))
            return vysledok
        cursor.execute("Select * from Shipment")  #
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok

    def stiahni(self, id):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Shipment WHERE id=?", [id])  #
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Date_time_close = data['Date_time_close']
        self.User_code = data['User_code']
        self.id = data['id']
        self.Customer_id = data['Customer_id']
        self.Vehicle_id = data['Vehicle_id']
        return self

    def nahraj(self, User_code, Date_time_close,Customer_id, Vehicle_id):  # Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.User_code = User_code
        self.Date_time_close = Date_time_close
        self.Customer_id = Customer_id
        self.Vehicle_id = Vehicle_id
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Shipment WHERE id = ?', [self.id])  #
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Shipment (id, Date_time_close, User_code, Customer_id, Vehicle_id) VALUES (?,?,?,?,?)',
                           (self.id, self.Date_time_close, self.User_code, self.Customer_id, self.Vehicle_id))  #
            cursor.execute("COMMIT")
            data = dict()
            data['User_code'] = self.User_code
            data['Date_time_close'] = self.Date_time_close
            data['id'] = self.id
            data['Customer_id'] = self.Customer_id
            data['Vehicle_id'] = self.Vehicle_id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Shipment", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None

    def update(self):
        if self.id:
            sql = """UPDATE Shipment SET User_code = ?, Date_time_close = ?, Customer_id = ?, Vehicle_id = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql, (self.User_code, self.Date_time_close,self.Customer_id,self.Vehicle_id, parse(str(datetime.datetime.now())), self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['User_code'] = self.User_code
            data['Date_time_close'] = self.Date_time_close
            data['id'] = self.id
            data['Customer_id'] = self.Customer_id
            data['Vehicle_id'] = self.Vehicle_id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Shipment", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None

class Work_statement():
    __tablename__ = "Work_statement"
    def __init__(self):
        self.User_code = None
        self.Work = None
        self.Time_start = None
        self.Time_end = None
        self.id = None

    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Work_statement")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Work_statement().stiahni(riadok[4]))
            return vysledok
        cursor.execute("Select * from Work_statement")  #
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok

    def stiahni(self, id):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Work_statement WHERE id=?", [id])  #
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.User_code = data['User_code']
        self.Work = data['Work']
        self.Time_start = data['Time_start']
        self.Time_end = data['Time_end']
        self.id = data['id']
        return self

    def nahraj(self, User_code, Work, Time_start, Time_end):  # Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Work = Work
        self.User_code = User_code
        self.Time_start = Time_start
        self.Time_end = Time_end
        self.id = str(uuid.uuid4())
        cursor.execute('SELECT * FROM Work_statement WHERE id = ?', [self.id])  #
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Work_statement (id, User_code, Work, Time_start, Time_end) VALUES (?,?,?,?,?)',
                           (self.id, self.User_code, self.Work,self.Time_start,self.Time_end))  #
            cursor.execute("COMMIT")
            data = dict()
            data['Work'] = self.Work
            data['User_code'] = self.User_code
            data['Time_start'] = self.Time_start
            data['Time_end'] = self.Time_end
            data['id'] = self.id
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Work_statement", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None

    def update(self):
        if self.id:
            sql = """UPDATE Work_statement SET User_code = ?, Work = ?, Time_start = ?, Time_end = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql, (self.User_code, self.Work, self.Time_start, self.Time_end, parse(str(datetime.datetime.now())), self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['User_code'] = self.User_code
            data['id'] = self.id
            data['Work'] = self.Work
            data['Time_start'] = self.Time_start
            data['Time_end'] = self.Time_end
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Work_statement", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None

class Stillage():
    __tablename__ = "Stillage"
    def __init__(self):
        self.Date_time_start = None
        self.Date_time_end = None
        self.Stillage_number = None
        self.Stillage_Number_on_Header = None
        self.First_scan_product = None
        self.Last_scan_product = None
        self.JLR_Header_NO = None
        self.Carriage_L_JLR_H = None
        self._Check = None
        self.First_scan_TLS_code = None
        self.Last_scan_TLS_code = None
        self.id = None
        self.Stillage_Type_id = None
        self.Shipment_id = None
        self.TLS_range_start = None
        self.TLS_range_stop = None
        self.Note = None


    def over_zmazanie(self):
        if(self.id ==None):
            return None
        over = overit_zmazanie(self.__tablename__,self.id)
        return over

    def zmazat(self,doplnok = ""):
        if (self.id == None):
            return None
        if doplnok == "":
            zmaz = zmaz_zaznam(self.__tablename__,self.id)
        else:
            zmaz = zmaz_zaznam(self.__tablename__, self.id,doplnok)
        return zmaz

    def vrat_vykonavatela(self):
        if self.id == None: return None
        return overit_vykonavatela(self.__tablename__,self.id)
    def nastav_vykonavatela(self,kod):
        if self.id == None or kod==None or isinstance(kod,int)==False:
            return None
        return vloz_vykonavatela(self.__tablename__, self.id,kod)


    def vrat_vsetky(self, klasy=False):  # Vypíše všetky riadky, vráti ako dictionary
        if klasy:
            cursor.execute("Select * from Stillage")  #
            vysledok = []
            for riadok in cursor.fetchall():
                vysledok.append(Stillage().stiahni(riadok[11]))
            return vysledok
        cursor.execute("Select * from Stillage")  #
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        return vysledok

    def stiahni(self, id):  # Vráti None ak neexistuje, inak vráti class
        cursor.execute("SELECT * FROM Stillage WHERE id=?", [id])  #
        col_name = [i[0] for i in cursor.description]
        test = cursor.fetchone()
        if test is None:
            return None
        data = dict(zip(col_name, test))
        self.Date_time_start = data['Date_time_start']
        self.Date_time_end = data['Date_time_end']
        self.Stillage_number = data['Stillage_number']
        self.Stillage_Number_on_Header = data['Stillage_Number_on_Header']
        self.First_scan_product = data['First_scan_product']
        self.Last_scan_product = data['Last_scan_product']
        self.JLR_Header_NO = data['JLR_Header_NO']
        self.Carriage_L_JLR_H = data['Carriage_L_JLR_H']
        self._Check = data['_Check']
        self.First_scan_TLS_code = data['First_scan_TLS_code']
        self.Last_scan_TLS_code = data['Last_scan_TLS_code']
        self.id = data['id']
        self.Stillage_Type_id = data['Stillage_Type_id']
        self.Shipment_id = data['Shipment_id']
        self.TLS_range_start = data['TLS_range_start']
        self.TLS_range_stop = data['TLS_range_stop']
        self.Note = data['Note']
        return self

    def nahraj(self, Date_time_start, Date_time_end, Stillage_number, Stillage_Number_on_Header, First_scan_product, Last_scan_product, JLR_Header_NO, Carriage_L_JLR_H, _Check, First_scan_TLS_code, Last_scan_TLS_code, Stillage_Type_id, Shipment_id, TLS_range_start, TLS_range_stop, Note):  # Ak záznam existuje vráti None, inak ho nahra do db a vrati class
        self.Date_time_start = Date_time_start
        self.Date_time_end = Date_time_end
        self.Stillage_number = Stillage_number
        self.Stillage_Number_on_Header = Stillage_Number_on_Header
        self.First_scan_product = First_scan_product
        self.Last_scan_product = Last_scan_product
        self.JLR_Header_NO = JLR_Header_NO
        self.Carriage_L_JLR_H = Carriage_L_JLR_H
        self._Check = _Check
        self.First_scan_TLS_code = First_scan_TLS_code
        self.Last_scan_TLS_code = Last_scan_TLS_code
        self.id = str(uuid.uuid4())
        self.Stillage_Type_id = Stillage_Type_id
        self.Shipment_id = Shipment_id
        self.TLS_range_start = TLS_range_start
        self.TLS_range_stop = TLS_range_stop
        self.Note = Note
        cursor.execute('SELECT * FROM Stillage WHERE id = ?', [self.id])  #
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute('INSERT INTO Stillage (id, Date_time_start, Date_time_end, Stillage_number, Stillage_Number_on_Header, First_scan_product, Last_scan_product, JLR_Header_NO, Carriage_L_JLR_H, _Check, First_scan_TLS_code, Last_scan_TLS_code, Stillage_Type_id, Shipment_id, TLS_range_start, TLS_range_stop, Note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (self.id, self.Date_time_start, self.Date_time_end,self.Stillage_number, self.Stillage_Number_on_Header, self.First_scan_product, self.Last_scan_product,self.JLR_Header_NO, self.Carriage_L_JLR_H, self._Check, self.First_scan_TLS_code, self.Last_scan_TLS_code, self.Stillage_Type_id, self.Shipment_id, self.TLS_range_start, self.TLS_range_stop, self.Note))  #
            cursor.execute("COMMIT")
            data = dict()
            data['Date_time_start'] = self.Date_time_start
            data['Date_time_end'] = self.Date_time_end
            data['Stillage_number'] = self.Stillage_number
            data['Stillage_Number_on_Header'] = self.Stillage_Number_on_Header
            data['First_scan_product'] =  self.First_scan_product
            data['Last_scan_product'] = self.Last_scan_product
            data['JLR_Header_NO'] = self.JLR_Header_NO
            data['Carriage_L_JLR_H'] = self.Carriage_L_JLR_H
            data['_Check'] = self._Check
            data['First_scan_TLS_code'] = self.First_scan_TLS_code
            data['Last_scan_TLS_code'] = self.Last_scan_TLS_code
            data['id'] = self.id
            data['Stillage_Type_id'] = self.Stillage_Type_id
            data['Shipment_id'] = self.Shipment_id
            data['TLS_range_start'] = self.TLS_range_start
            data['TLS_range_stop'] = self.TLS_range_stop
            data['Note'] = self.Note
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Stillage", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        else:
            return None

    def update(self):
        if self.id:
            sql = """UPDATE Stillage SET Date_time_start = ?, Date_time_end = ?, Stillage_number = ?, Stillage_Number_on_Header = ?, First_scan_product = ?, Last_scan_product = ?, JLR_Header_NO = ?, Carriage_L_JLR_H = ?, _Check = ?, First_scan_TLS_code = ?, Last_scan_TLS_code = ?, Stillage_Type_id = ?, Shipment_id = ?, TLS_range_start = ?, TLS_range_stop = ?, Note = ?, last_sync = ? WHERE id = ?"""
            cursor.execute(sql, (self.Date_time_start, self.Date_time_end,self.Stillage_number, self.Stillage_Number_on_Header, self.First_scan_product, self.Last_scan_product,self.JLR_Header_NO, self.Carriage_L_JLR_H, self._Check, self.First_scan_TLS_code, self.Last_scan_TLS_code, self.Stillage_Type_id, self.Shipment_id, self.TLS_range_start, self.TLS_range_stop, self.Note, parse(str(datetime.datetime.now())), self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Date_time_start'] = self.Date_time_start
            data['Date_time_end'] = self.Date_time_end
            data['Stillage_number'] = self.Stillage_number
            data['Stillage_Number_on_Header'] = self.Stillage_Number_on_Header
            data['First_scan_product'] =  self.First_scan_product
            data['Last_scan_product'] = self.Last_scan_product
            data['JLR_Header_NO'] = self.JLR_Header_NO
            data['Carriage_L_JLR_H'] = self.Carriage_L_JLR_H
            data['_Check'] = self._Check
            data['First_scan_TLS_code'] = self.First_scan_TLS_code
            data['Last_scan_TLS_code'] = self.Last_scan_TLS_code
            data['id'] = self.id
            data['Stillage_Type_id'] = self.Stillage_Type_id
            data['Shipment_id'] = self.Shipment_id
            data['TLS_range_start'] = self.TLS_range_start
            data['TLS_range_stop'] = self.TLS_range_stop
            data['Note'] = self.Note
            data['last_sync'] = str(parse(str(datetime.datetime.now())))
            try:
                client_server_nahraj_jeden("Stillage", data)  #
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
            return self
        return None

if __name__ == '__main__':
    start_time = time.time()
    #synchronize_db_server_client()
    print("--- %s seconds ---" % (time.time() - start_time))