import socket #Importa la libreria "Socket" necessaria per l'instaurazione della comunicazione, sia con protocollo UDP che TCP.
from time import ctime #Permette di ottenere il tempo in secondi come stringa
from datetime import datetime #Permette di ottenere il time-stamp locale del PC

host='localhost' #importa l'host del server a quello default locale del PC
data_payload=2048 #dimensione del buffer di comunicazione (bytes)
#________________________________________________________________________________________________
#FUNZIONE: TIME-STAMP
def time_stamp():
    now=datetime.now().time() #Salvataggio dell'ora locale prima dell'invio
    sec=now.second #Separazione dei secondi
    us=now.microsecond #Separazione dei microsecondi
    return sec,us

#FUNZIONE: ECHO CLIENT
def echo_client(port,n_test):
    file=open("Istanti_client_udp.csv","a") #Apriamo il file .csv relativo agli istanti temporali
                                            #di invio e ricezione dei messaggi in modo da poterli elaborare
    file.write("Inviato;Ricevuto;\n") #Nome delle due colonne del file .csv
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creazione del socket udp
    server_addr=(host,port) #Definizione dell'indirizzo del server
    msg="Messaggio di test."
    for i in range(n_test): #Loop che itera l'invio del messaggio di test
        sec1,us1=time_stamp()
        sent=sock.sendto(msg.encode('utf-8'),server_addr) #Invio del messaggio
        data,server=sock.recvfrom(data_payload) #Ascolto e ricezione del messaggio dal server
        sec2,us2=time_stamp()
        file.write(str(sec1)+'.'+str(us1)+';') #Scrittura sul file csv del time-stamp di invio 
        file.write(str(sec2)+'.'+str(us2)+";\n") #Scrittura sul file csv del time-stamp di ricezione
    sock.close()
    file.close()
    
#__________________________________________________________________________________________________________
if __name__=='__main__':
    echo_client(9900,10)