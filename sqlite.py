import sqlite3
import requests
from tqdm import tqdm
db = sqlite3.connect("gefco.db")
cursor = db.cursor()
def synchronize_db():
    tabulky = ["General","User_Role","Customer","Vehicle","User","Config","Shipment","Pattern","Work_statement","Stillage_type","Advanced_user","Stillage","Pattern_Item"] #Vsetky tabulky
    #tabulky = ["Config"] # len jedna tabulka, pre test
    for nazov_tabulky in tabulky:
        URL = "http://127.0.0.1:5100/"
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


if __name__ == '__main__':
    synchronize_db()
