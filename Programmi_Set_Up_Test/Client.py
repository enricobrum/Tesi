#Client TCP utilizzato per l'invio dei messaggi verso
#il server avviato sul dispositivo che distribuisce
#la rete 5G e contiene al suo interno la realizzazione
#tramite Docker delle funzioni di rete necessarie per 
#il funzionamento dell'infrastruttura 5G privata.
#_________________________________________________________
from datetime import date
import socket #libreria necessaria all'utilizzo dei 
              #protocolli di comunicazione
import argparse #libreria necessaria all'utilizzo degli 
                #argomenti nella chiamata a funzione
import Utility #libreria personale contenente la funzione
               #"time_stamp()" che permette di estrarre i
               #secondi e microsendi dall'orologio locale
#________________________________________________________
#Funzione per avviare il client tcp tentando la connessione
#con l'indirizzo IP del server passato come argomento, la 
#porta in cui e' in ascolto e la dimensione, in byte, del 
#messaggio da inviare. Infine e' anche passata la tipologia
#di test che si sta effettuando in modo da tenere conto 
#dello scenario da cui provengono i futuri dati raccolti
def tcp_client(server_host,server_port,payload_size,type_test):
    filecsv="istanti_temporali_"+str(date.isoformat)+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("Inviato,Ricevuto,PackSize,Traffico,RTT\n")
        print("File csv creato.")









#_________________________________________________________________
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client")
    parser.add_argument('--server_host', default='127.0.0.1', help='Server host')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--payload_size', type=int, default=1024, help='Payload size in bytes')
    parser.add_argument('--type_test', default='no-traffico',help='Tipologia di test')
    args = parser.parse_args()

    tcp_client(args.server_host, args.server_port, args.payload_size, args.type_test)
       