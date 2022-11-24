import json
import uuid
import time
import sqlite3
import requests
db = sqlite3.connect("gefco.db")
cursor = db.cursor()
tabulky = ["General", "User_Role", "Customer", "Vehicle", "User", "Config", "Shipment", "Pattern", "Work_statement","Stillage_type", "Advanced_user", "Stillage", "Pattern_Item"]  # Vsetky tabulky

#tabulky = ["Stillage"] # len jedna tabulka, pre test
def synchronize_db_server_client():
    for nazov_tabulky in tabulky:
        URL = "http://server.nahovno.eu:5100/Get"
        post = {
            "api-heslo": "YouWontGuessThisOne",
            "tabulka": f"{nazov_tabulky}"
        }
        r = requests.post(url=URL, json=post,timeout=None)
        data = r.json()
        cursor.execute("begin")
        for i in data:
            #Zacinam kontrolu, či sa zaznam nachadza už v lokalnej db
            if(nazov_tabulky=="User"):
                over_uuid = """SELECT EXISTS(SELECT 1 FROM %s WHERE code = '%s')""" % (nazov_tabulky,i.get("code"))
            else:
                over_uuid = """SELECT EXISTS(SELECT 1 FROM %s WHERE id = '%s')""" % (nazov_tabulky,i.get("id"))
            cursor.execute(over_uuid)
            #nachadza sa, skipujem
            if cursor.fetchone() == (1,):
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
    for nazov_tabulky in tabulky:
        cursor.execute("""SELECT * FROM %s""" % (nazov_tabulky))
        col_name = [i[0] for i in cursor.description]
        vysledok = []
        for riadok in cursor.fetchall():
            temp = dict(zip(col_name, riadok))
            vysledok.append(temp)
        #print(nazov_tabulky,temp)
        URL = "http://server.nahovno.eu:5100/Post"
        post = {
            "api-heslo": "YouWontGuessThisOne",
            "tabulka": f"{nazov_tabulky}",
            "data" : vysledok
        }
        r = requests.post(url=URL, json=post, timeout=None)
        print(f"Nahrávam {nazov_tabulky}")
        print(r.text) #Aby som nesiel príliš rýchlo, potom sa nestihnú tabulky spracovat v spravnom poradí a to vedie k zlým foreign keys

def client_server_nahraj_jeden(nazov_tabulky,data):
    vysledok = [data]
    URL = "http://server.nahovno.eu:5100/Post"
    post = {
        "api-heslo": "YouWontGuessThisOne",
        "tabulka": f"{nazov_tabulky}",
        "data" : vysledok
    }
    r = requests.post(url=URL, json=post, timeout=None)
    return r.text

#Tu zacinaju tabulky ako classy --------------------------------------------------------------------------------------------------------------------
class Customer:
    def __init__(self):
        self.Name = None
        self.id = None
    def vrat_vsetky(self): # Vypíše všetky riadky
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
            sql = """UPDATE CUSTOMER SET Name= '%s' WHERE id = '%s'""" % (self.Name,self.id)
            cursor.execute(sql)
            cursor.execute("COMMIT")
            data = dict()
            data['id'] = self.id
            data['Name'] = self.Name
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
    def __int__(self):
        self.Last_changes = None
        self.Last_available = None
        self.Automatic_export = None
        self.id = None
    def vrat_vsetky(self): # Vypíše všetky riadky, vráti ako dictionary
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
            data['Last_changes'] = self.Last_changes
            data['Last_available'] = self.Last_available
            data['Automatic_export'] = self.Automatic_export
            data['id'] = self.id
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
            sql = """UPDATE General SET Last_changes= ?,Last_available=?,Automatic_export = ? WHERE id = ?"""
            cursor.execute(sql,(self.Last_changes,self.Last_available,self.Automatic_export,self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Last_changes'] = self.Last_changes
            data['Last_available'] = self.Last_available
            data['Automatic_export'] = self.Automatic_export
            data['id'] = self.id
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
    def __int__(self):
        self.Name = None
        self.id = None
    def vrat_vsetky(self): # Vypíše všetky riadky, vráti ako dictionary
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
            sql = """UPDATE Stillage_type SET Name = ? WHERE id = ?"""
            cursor.execute(sql,(self.Name,self.id))
            cursor.execute("COMMIT")
            data = dict()
            data['Name'] = self.Name
            data['id'] = self.id
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


# class User_Role(Base, SerializerMixin):
#     __tablename__ = 'User_Role'
#
#     name = Column(Text)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#
#
# class Vehicle(Base, SerializerMixin):
#     __tablename__ = 'Vehicle'
#
#     SPZ = Column(Text)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#
#
# class Config(Base, SerializerMixin):
#     __tablename__ = 'Config'
#
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Customer_id = Column(ForeignKey('Customer.id'))
#     Vehicle_id = Column(ForeignKey('Vehicle.id'))
#
#     #Customer = relationship('Customer')
#     #Vehicle = relationship('Vehicle')
#
#
# class Pattern(Base, SerializerMixin):
#     __tablename__ = 'Pattern'
#
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Customer_id = Column(ForeignKey('Customer.id'))
#
#     #Customer = relationship('Customer')
#
#
# class User(Base, SerializerMixin):
#     __tablename__ = 'User'
#
#     code = Column(BigInteger, primary_key=True)
#     Name = Column(Text)
#     Last_name = Column(Text)
#     User_Role_id = Column(ForeignKey('User_Role.id', match='FULL'))
#
#     #User_Role = relationship('UserRole')
#
#
# class Advanced_user(Base, SerializerMixin):
#     __tablename__ = 'Advanced_user'
#
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Config_id = Column(ForeignKey('Config.id'))
#     User_code = Column(ForeignKey('User.code'))
#
#     #Config = relationship('Config')
#     #User = relationship('User')
#
#
# class Pattern_Item(Base, SerializerMixin):
#     __tablename__ = 'Pattern_Item'
#
#     Number = Column(BigInteger)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Pattern_id = Column(ForeignKey('Pattern.id'))
#     Stillage_type_id = Column(ForeignKey('Stillage_type.id'))
#
#     #Pattern = relationship('Pattern')
#     #Stillage_type = relationship('StillageType')
#
#
# class Shipment(Base, SerializerMixin):
#     __tablename__ = 'Shipment'
#
#     User_code = Column(ForeignKey('User.code'))
#     Date_time_close = Column(DateTime)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Customer_id = Column(ForeignKey('Customer.id'))
#     Vehicle_id = Column(ForeignKey('Vehicle.id'))
#
#     #Customer = relationship('Customer')
#     #User = relationship('User')
#     #Vehicle = relationship('Vehicle')
#
#
# class Work_statement(Base, SerializerMixin):
#     __tablename__ = 'Work_statement'
#
#     User_code = Column(ForeignKey('User.code'))
#     Work = Column(BigInteger)
#     Time_start = Column(DateTime)
#     Time_end = Column(DateTime)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#
#     #User = relationship('User')
#
#
# class Stillage(Base, SerializerMixin):
#     __tablename__ = 'Stillage'
#
#     Date_time_start = Column(DateTime)
#     Date_time_end = Column(DateTime)
#     Stillage_number = Column(BigInteger)
#     Stillage_Number_on_Header = Column(BigInteger)
#     First_scan_product = Column(BigInteger)
#     Last_scan_product = Column(BigInteger)
#     JLR_Header_NO = Column(BigInteger)
#     Carriage_L_JLR_H = Column('Carriage_L_JLR_H', Text)
#     _Check = Column(BigInteger)
#     First_scan_TLS_code = Column(BigInteger)
#     Last_scan_TLS_code = Column(BigInteger)
#     id = Column(Text, primary_key=True, server_default=text("uuid_in((md5(((random())::text || (random())::text)))::cstring)"))
#     Stillage_Type_id = Column(ForeignKey('Stillage_type.id'))
#     Shipment_id = Column(ForeignKey('Shipment.id'))
#     TLS_range_start = Column(BigInteger)
#     TLS_range_stop = Column(BigInteger)
#     Note = Column(Text)
#
#     #Shipment = relationship('Shipment')
#     #Stillage_Type = relationship('StillageType')

if __name__ == '__main__':
    start_time = time.time()
    #synchronize_db_server_client()
    print("--- %s seconds ---" % (time.time() - start_time))
