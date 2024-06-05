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
    while True:
        comando = input("-> ")
        if comando == "ESC":
            s.close()
            sys.exit()
        if comando == "test":
            file=open("Istanti_Temporali_CLIENT_TCP.txt","a")
            file.write("\nInviato: \n")
            time=str(datetime.now().time().second)+"s"+str(datetime.now().time().microsecond)+"us"   
            file.write(time)
            s.send(comando.encode())
            data=s.recv(4096) #4096 byte dimensione del buffer
            file.write("\nRicevuto:\n")
            time=str(datetime.now().time().second)+"s"+str(datetime.now().time().microsecond)+"us"   
            file.write(time)
            print("Ricevuto")
            file.close()
          
            
def conn_sub_server(indirizzo_server):
    try:
        s=socket.socket() #creazione socket client
        s.connect(indirizzo_server)
        print(f"connessione al server {indirizzo_server} stabilita")
    except socket.error as errore:
        print(f"qualcosa è andato storto, sto uscendo...\n {errore}")
        sys.exit()
    richiesta(s)
    
if __name__=="__main__":
    conn_sub_server(("127.0.0.1",20000))
