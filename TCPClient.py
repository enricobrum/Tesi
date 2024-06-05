# Creazione CLIENT SOCKET:
#--------------------------------
# 1 - Creazione socket                      # socket.socket()
# 2 - Connessione al Server                 # connect(indirizzo)
# 3 - Invio di una Richiesta al Server      # send()
# 4 - Ricezione della Risposta dal Server   # recv()# Funzioni Generiche:
#--------------------------------
# s.recv()                => Riceve messaggi TCP
# s.send()                => Trasmette messaggi TCP
# s.close()               => Chiude il Socket
# socket.gethostname()    => Restituisce l'hostname della macchina su cui sta girando l'Interprete di Python
# socket.gethostbyname()  => Restituisce l'IP associato al nome passato
# Funzioni Client Socket:
#--------------------------------
# s.connect()    => Inizia la connessione col Server. Richiede un Tuple contenente IP e Porta del Servizio
import socket 
import sys 
from time import ctime
from datetime import datetime

def richiesta(s):
        data=datetime.now().time().microsecond #assegna come dato da mandare il timestamp in microsecondi di invio
        s.send(str(data).encode("utf-8"))
        data=s.recv(4096) #4096 byte dimensione del buffer
        print(data.decode()+','+str(datetime.now().time().microsecond))

            
def conn_sub_server(indirizzo_server):
    try:
        s=socket.socket() #creazione socket client
        s.connect(indirizzo_server)
        print(f"connessione al server {indirizzo_server} stabilita")
    except socket.error as errore:
        print(f"qualcosa è andato storto, sto uscendo...\n {errore}")
        sys.exit()
    richiesta(s)
