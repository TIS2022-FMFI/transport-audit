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

if __name__ == "__main__" :
    print(citaj_report())


