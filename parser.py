import csv

def citaj_report():
    with open('report.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        pointer = 0
        hlava = []
        vysledok = {}
        for row in reader_obj:
            if pointer==0:
                hlava = row[0].split(",")
            else:
                pointrik = 0
                k = dict()
                for slovo in row[0].split(","):
                    k[hlava[pointrik]] = slovo
                    pointrik+=1
                if k['carriagefullno'] not in vysledok:
                    vysledok[k['carriagefullno']] = []
                vysledok[k['carriagefullno']].append(k)

            pointer +=1
    for polozkyVozika in vysledok.values(): #ak nahodou v reporte nie su polozky vozika v spravnom poradi
        polozkyVozika.sort(key = lambda x : int(x['position']))
    return vysledok

if __name__ == "__main__" :
    vysl = citaj_report()
    print(len(vysl))

    for k, v in vysl.items():
        print(k)
        for vv in v:
            print(vv)
        print()

    print("\n\n")
    print(vysl['0113015417677'][0])
    print(vysl['0113015417677'][-1])


