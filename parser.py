import csv
import requests
from config import sync_URL,api_password
from logy import logni
def ziskaj_report(user_code):
    URL = f"{sync_URL}/Report"
    post = {
        "api-heslo": f"{api_password}"
    }
    try:
        r = requests.post(url=URL, json=post, timeout=None)
        open('report.csv', 'wb').write(r.content)
        return True
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        logni(user_code,201,str(errh))
        return False
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        logni(user_code, 202, str(errc))
        return False
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        logni(user_code, 203, str(errt))
        return False
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
        logni(user_code, 0, str(err))
        return False


def citaj_report():
    with open('report.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        pointer = 0
        hlava = []
        vysledok = []
        for row in reader_obj:
            if pointer==0:
                hlava = row[0].split(",")
            else:
                pointrik = 0
                k = dict()
                for slovo in row[0].split(","):
                    k[hlava[pointrik]] = slovo
                    pointrik+=1
                vysledok.append(k)

            pointer +=1
    return vysledok

def citaj_report_dict(): #Vracia ako dictionary
    with open('report.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        pointer = 0
        hlava = []
        vysledok = {}
        for row in reader_obj:
            if pointer == 0:
                hlava = row[0].split(",")
            else:
                pointrik = 0
                k = dict()
                for slovo in row[0].split(","):
                    k[hlava[pointrik]] = slovo
                    pointrik += 1
                if k['carriagefullno'] not in vysledok:
                    vysledok[k['carriagefullno']] = []
                vysledok[k['carriagefullno']].append(k)

            pointer += 1
    for polozkyVozika in vysledok.values():  # ak nahodou v reporte nie su polozky vozika v spravnom poradi
        polozkyVozika.sort(key=lambda x: int(x['position']))
    return vysledok
if __name__ == "__main__" :
    print(ziskaj_report(1234))


