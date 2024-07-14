#Client TCP utilizzato per l'invio dei messaggi verso
#il server avviato sul dispositivo che distribuisce
#la rete 5G e contiene al suo interno la realizzazione
#tramite Docker delle funzioni di rete necessarie per 
#il funzionamento dell'infrastruttura 5G privata.
#_________________________________________________________
from datetime import datetime 
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
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("Inviato,Ricevuto,PackSize,Traffico,RTT\n")
        print("File csv creato.")
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host,server_port))
        #   print(f"Connessione al server TCP {server_host}:{server_port}")
            payload=b'a'*payload_size
            sec1,us1=Utility.time_stamp()
            client_socket.sendall(payload)
        #   print(f"Inviati {payload_size} bytes")
            data=client_socket.recv(65536) #buffer impostato al massimo
            #in modo da effettuare test con variazione del payload
            sec2,us2=Utility.time_stamp()
            file.write(str(sec1)+'.'+str(us1)+',')
            file.write(str(sec2)+'.'+str(us2)+',')
            file.write(str(payload_size)+','+type_test+',')
            rtt_sec=sec2-sec1
            if rtt_sec >= 0:
                rtt_us=us2-us1
            else:
                rtt_us=(us2-us1)
            file.write(str(rtt_us))
            file.write("\n")
        #   print(f"Ricevuto {len(data)} bytes da {server_host}:{server_port}")
            file.close()
    except Exception as e:
        print(f"Eccezione {e} durante la connessione con il server.")


#_________________________________________________________________
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client")
    parser.add_argument('--server_host', default='127.0.0.1', help='Server host')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--payload_size', type=int, default=1024, help='Payload size in bytes')
    parser.add_argument('--type_test', default='no-traffico',help='Tipologia di test')
    args = parser.parse_args()

    tcp_client(args.server_host, args.server_port, args.payload_size, args.type_test)
       