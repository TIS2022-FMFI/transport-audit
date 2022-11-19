import json
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



if __name__ == '__main__':
    start_time = time.time()
    synchronize_db_client_server()

    print("--- %s seconds ---" % (time.time() - start_time))
