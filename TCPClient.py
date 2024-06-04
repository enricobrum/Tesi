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

def invia_comandi(s):
    while True:
        comando=input("-> ")
        if comando=="ESC":
            print("sto chiudendo la connessione")
            s.close()
            sys.exit()
        else:
            s.send(comando.encode())
            data=s.recv(4096) #4096 byte dimensione del buffer
            print(str(data,"utf-8"))
            
def conn_sub_server(indirizzo_server):
    try:
        s=socket.socket() #creazione socket client
        s.connect(indirizzo_server)
        print(f"connessione al server {indirizzo_server} stabilita")
    except socket.error as errore:
        print(f"qualcosa è andato storto, sto uscendo...\n {errore}")
        sys.exit()
    invia_comandi(s)
    
if __name__=="__main__": #se stiamo lanciando questo script come programma
        conn_sub_server(("127.0.0.1",20000))