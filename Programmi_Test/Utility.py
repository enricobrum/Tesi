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
# (1-Comunicazione UDP solamente tra client-server senza ulteriore traffico. Client e Server presenti
#   sulla stessa macchina: UDP1)
# 2-Comunicazione UDP solamente tra client-server senza ulteriore traffico variando la dimensione del payload.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su
#   dispositivo connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: UDP
# 3-Comunicazione UDP solamente tra client-server variando la dimensione del payload con traffico generato tramite IPERF.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su dispositivo
#   connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: UDP_IPERF (Da definire tipologia di traffico)
# 4-Comunicazione TCP solamente tra client-server senza ulteriore traffico variando la dimensione del payload.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su
#   dispositivo connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: TCP
# 5-Comunicazione TCP solamente tra client-server variando la dimensione del payload con traffico generato tramite IPERF.
#   Client e Server presenti su macchine diverse, server sulla macchina contenente il core-network e client su dispositivo
#   connesso alla rete (Raspberry, PC) tramite i moduli Quectel.
#   NOME TEST: TCP_IPERF (Da definire tipologia di traffico)
# 6-Comunicazione HTTP in cui il Server viene avviato sul computer contente il core-network e Client su dispositivo esterno connesso
#   alla rete 5G Firecell (Raspberry,PC) tramite i moduli Quectel senza la presenza del traffico aggiuntivo.
#   NOME TEST: HTTP
#   # 6-Comunicazione HTTP in cui il Server viene avviato sul computer contente il core-network e Client su dispositivo esterno connesso
#   alla rete 5G Firecell (Raspberry,PC) tramite i moduli Quectel con la presenza del traffico aggiuntivo.
#   NOME TEST: HTTP_IPERF (Da definire la tipologia di traffico)