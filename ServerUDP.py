import socket #Importa la libreria "Socket" necessaria per l'instaurazione della comunicazione, sia con protocollo UDP che TCP.
from time import ctime #Permette di ottenere il tempo in secondi come stringa
from datetime import datetime #Permette di ottenere il time-stamp locale del PC

host='localhost' #importa l'host del server a quello default locale del PC
data_payload=2048 #dimensione del buffer di comunicazione (bytes)
#________________________________________________________________________________________________
#FUNZIONE: ECHO SERVER
#Funzione che permette di avviare un server sulla porta passata come parametro "port" e che ha la
#sola funzione di effettuare un echo dei messaggi che riceve nel buffer.
def echo_server(port):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Crea il socket UDP
    server_addr=(host,port) #Definisco l'indirizzo del server 
    print("Inizializzo Echo Server on %s port %s ...\n" % server_addr)
    sock.bind(server_addr) #Inizializza il server sull'indirizzo passato come argomento
    print("Server in funzione.\n")
    while True:
        data,addr=sock.recvfrom(data_payload) #Il server si mette in ascolto con un buffer di dimensione indicata dalla variabile
        if data:    
            print(data.decode())
            sent=sock.sendto(data,addr) #Rimanda indietro il messaggio arrivato
            print("Messaggio rispedito.\n")
    sock.close() #Chiusura del socket
#______________________________________________________________________________________________________________


