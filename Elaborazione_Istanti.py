import time
from time import ctime
from datetime import datetime

def Elaborazione(testo):
    file=open(testo,"r")
    tmp1=file.readlines()
    file.close()
    for i in tmp1.__len__:
        tmp1.remove("Inviato: \n")
        tmp1.remove("Ricevuto:\n")
        print(tmp1)
    
    
if __name__=="__main__":
    Elaborazione("Istanti_Temporali_CLIENT_TCP.txt")
    