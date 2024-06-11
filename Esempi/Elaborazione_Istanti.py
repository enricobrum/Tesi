#File di elaborazione degli istanti temporali contenuti all'interno dei relativi file .csv.
#Se lanciato su i file relativi al Client il risultato rappresenterà il Round Trip Time essendo la differenza tra l'istante di invio e l'istante
#di ricezione del messaggio di risposta del server. Se lanciato su i file relativi al Server permetterà di capire il tempo impiegato da esso a 
#rispondere.
import csv
import sys

def Elaborazione(file):
    with open(file, newline="\n") as filecsv:
        lettore = csv.reader(filecsv,delimiter=";")
        line_count=0
        for row in lettore:
            print(row)
            if line_count == 0:
                line_count += 1
            else:
                invio=float(row[0])
                ricezione=float(row[1])
                RTT=ricezione-invio
                print(RTT)
                line_count += 1

if __name__=="__main__":
    Elaborazione(sys.argv[1])