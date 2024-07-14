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
#TIPOLOGIA DI TEST:
# 1-Comunicazione TCP solamente tra client-server senza ulteriore traffico variando la dimensione del payload.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su
#   dispositivo connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: TCP
# 2-Comunicazione TCP solamente tra client-server variando la dimensione del payload con traffico generato tramite IPERF.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su dispositivo
#   connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: TCP_IPERF*{tipo traffico}
# 2.1-Definire come variare il traffico e porre diverse situazioni



