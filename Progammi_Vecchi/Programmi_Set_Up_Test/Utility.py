from time import ctime #Permette di ottenere il tempo in secondi come stringa
from datetime import datetime #Permette di ottenere il time-stamp locale del PC
#________________________________________________________________________________________________
#FUNZIONE: TIME-STAMP
def time_stamp():
    now=datetime.now().time() #Salvataggio dell'ora locale prima dell'invio
    sec=now.second #Separazione dei secondi
    us=now.microsecond #Separazione dei microsecondi
    return sec,us

#_______________________________________________________________________________________________



