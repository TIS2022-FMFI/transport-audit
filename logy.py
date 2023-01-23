import datetime
import os
import sqlite3
import uuid

import requests

import config
db_path_logy = os.path.abspath(os.path.dirname(__file__)) + "/logy.db"
db_path_logy = os.path.normpath(db_path_logy)
db_logy = sqlite3.connect(db_path_logy)
cursor_logy = db_logy.cursor()

def nahraj_log_na_server(data):
    try:
        if (config.allow_synchronize == False): return False
        vysledok = [data]
        URL = f"{config.sync_URL}/Log"
        post = {
            "api-heslo": f"{config.api_password}",
            "tabulka": f"logy",
            "data": vysledok
        }
        r = requests.post(url=URL, json=post, timeout=None)
        return r.text
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
def logni(user_code,kod_chyby=0,chyba=""):
    id = str(uuid.uuid4())
    android = 1
    cas = str(datetime.datetime.now())
    cursor_logy.execute('INSERT INTO logy (id, kod_chyby, chyba,uzivatel,android,doplnok) VALUES (?,?,?,?,?,?)',
                   (id, kod_chyby, chyba,str(user_code),android,cas))
    cursor_logy.execute("COMMIT")
    data = dict()
    data['id'] = id
    data['kod_chyby'] = kod_chyby
    data['chyba'] = chyba
    data['uzivatel'] = str(user_code)
    data['android'] = android
    data['doplnok'] = cas
    nahraj_log_na_server(data)

def logy_nahraj_vsetky_na_server():
    cursor_logy.execute("""SELECT * FROM %s""" % ("logy"))
    col_name = [i[0] for i in cursor_logy.description]
    for riadok in cursor_logy.fetchall():
        temp = dict(zip(col_name, riadok))
        nahraj_log_na_server(temp)
if __name__ == '__main__':
    print(db_logy.execute("SELECT * FROM logy").fetchall())