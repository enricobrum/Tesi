#Client TCP utilizzato per l'invio dei messaggi verso
#il server avviato sul dispositivo che distribuisce
#la rete 5G e contiene al suo interno la realizzazione
#tramite Docker delle funzioni di rete necessarie per 
#il funzionamento dell'infrastruttura 5G privata.
#_________________________________________________________
from datetime import datetime
from ping3 import ping
import time
import socket #libreria necessaria all'utilizzo dei 
              #protocolli di comunicazione
import argparse #libreria necessaria all'utilizzo degli 
                #argomenti nella chiamata a funzione
import Utility #libreria personale contenente la funzione
               #"time_stamp()" che permette di estrarre i
               #secondi e microsendi dall'orologio locale
#________________________________________________________
#Definizione delle costanti utilizzate per i test
#Dimensione del payload (byte)
PAYLOAD=[8,16,32,64,128,256,512,1024,1500]
#Funzione per avviare il client tcp tentando la connessione
#con l'indirizzo IP del server passato come argomento, la 
#porta in cui e' in ascolto e la dimensione, in byte, del 
#messaggio da inviare. Infine e' anche passata la tipologia
#di test che si sta effettuando in modo da tenere conto 
#dello scenario da cui provengono i futuri dati raccolti
#Vettore contenente gli intertempi di test
INTERTEMPO=[0.01,0.1,1,5,10]
#Funzione per connettersi al server
def connect_to_server(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket
    except Exception as e:
        print(f"Errore nella connessione al server: {e}")
        return None
#Funzione per selezionare la tipologia di test
def select_test():
    print("Seleziona il test da eseguire:")
    print("1. Test variazione payload e intertempo")
    print("2. Test variazione payload e intertempo + traffico Iperf")
    print("3. Test di throughput (sfruttando libreria 'ping3' python)")
    print("4. Test di latenza (sfruttando la libreria 'time' di python)")
    choice = input("Inserisci il numero del test: ")
    return choice
#Funzione di test di variazione payload e intertempo
def test_payload_inter(client_socket,file,type_test):
    #Impostiamo il messaggio da inviare pari ai byte del payload
    for intertempo in INTERTEMPO:
        for payload_size in PAYLOAD:
            payload=b'a'*payload_size
            sec1,us1=Utility.time_stamp()
            tempo_avvio = time.time()
            client_socket.sendall(payload)
            data=client_socket.recv(65536)
            sec2,us2=Utility.time_stamp()
            file.write(str(sec1)+'.'+str(us1)+',')
            file.write(str(sec2)+'.'+str(us2)+',')
            file.write(str(payload_size)+','+type_test+',')
            if sec2 - sec1 == 0:
                rtt_us=us2-us1
            else:
                rtt_us=us1-us2+1000000
            file.write(str(rtt_us))
            file.write("\n")
            tempo_rimanente = time.time() - tempo_avvio
            time.sleep(intertempo-tempo_rimanente)
          
#Funzione principale del client
def tcp_client(server_host,server_port,payload_size,type_test):
    client_socket = connect_to_server(server_host,server_port)
    if not client_socket:
        print("Impossibile connettersi al server. Uscita.")
        return
    else:
        data_corrente = datetime.now()
        data_stringa = data_corrente.strftime("%Y-%m-%d")
        filecsv="istanti_temporali_"+data_stringa+".csv"
        file=open(filecsv,"a")
        if file.tell()==0:
            file.write("Inviato,Ricevuto,PackSize,Traffico,RTT\n")
            print("File csv creato.")
        while True:
            ntest = select_test()
            if ntest == '1':
                test_payload_inter(client_socket,file,type_test)
            elif ntest == '2':
                continue
            elif ntest == '3':
                continue                
            elif ntest == '4':
                continue
            else:
                print("Scelta non valida.")
                continue
    



#_________________________________________________________________
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client")
    parser.add_argument('--server_host', default='127.0.0.1', help='Server host')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--payload_size', type=int, default=1024, help='Payload size in bytes')
    parser.add_argument('--type_test', default='no-traffico',help='Tipologia di test')
    args = parser.parse_args()

    tcp_client(args.server_host, args.server_port, args.payload_size, args.type_test)
       