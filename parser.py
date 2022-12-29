import csv

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
    print(citaj_report())
    print(citaj_report_dict())


