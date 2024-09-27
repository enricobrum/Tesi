import ntplib 
from time import ctime  
import socket
import time
import argparse
import subprocess
from datetime import datetime

def get_ntp_timestamp(ntp_client):
    server = 'ntp1.inrim.it'
    try: 
        response = ntp_client.request(server, version=4)
    except Exception as e:
        istante = 0
    return response  # Tempo in secondi

def test_ntp(client_socket,ntp_client,host,port):
    # Ottieni il timestamp prima di inviare il messaggio
    client_send_timestamp = get_ntp_timestamp(ntp_client)
    #print(f"Timestamp invio client (secondi): {client_send_timestamp}")
    # Invia il messaggio al server
    client_socket.sendall("Richiesta dal client".encode())
    # Attende la risposta del server
    data, _ = client_socket.recvfrom(1024)
    # Ottieni il timestamp corrente del client per il calcolo dell'RTT
    client_receive_timestamp = get_ntp_timestamp(ntp_client)
    server_timestamp = float(data.decode())  # Converte il timestamp dal server 
    #print(f"Timestamp ricezione client (secondi): {client_receive_timestamp}")
    # Calcola l'RTT (Round Trip Time)
    rtt = (client_receive_timestamp.tx_time - client_send_timestamp.tx_time) - client_send_timestamp.delay - client_receive_timestamp.delay
    print(f"RTT (Round Trip Time) in secondi: {rtt:.6f}")
    # Calcola l'OTT (One Trip Time)
    ott = ((server_timestamp - client_send_timestamp.tx_time) + (client_receive_timestamp.tx_time - server_timestamp)- client_send_timestamp.delay - client_receive_timestamp.delay) / 2 
    print(f"OTT (One Trip Time) in secondi: {ott:.6f}")
    return rtt,ott
#Funzione utilizzata per l'invio e l'attesa della risposta di messaggi TCP e
#il calcolo del relativo Round Trip Time. 
def send_recv_rtt(client_socket,message):

    client_socket.sendall(message.encode('utf-8'))
    start_time = time.time()

    response = client_socket.recv(65536)
    end_time = time.time()
    rtt= end_time - start_time
    return rtt,response

#Funzione per la connessione TCP con il server
def connect_to_server(host, port):
    """
    Crea e stabilisce una connessione TCP con il server specificato.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server e' in ascolto.

    Returns:
        socket: Oggetto socket connesso al server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connesso al server {host}:{port}")
    return client_socket

        
#Funzione di test utilizzando il comando "ping"
def ping_test_subprocess(host, file, traffic):
    """
    Esegue un test di ping al server utilizzando subprocess per aggirare i problemi di permessi.

    Args:
        host (str): Indirizzo IP del server.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
    """
    num_pings=100
    print(f"Eseguendo ping verso {host} utilizzando subprocess...")
    for _ in range(num_pings):
        file.write("ping"+','+str(traffic)+',')
        try:
            result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                # Estrarre l'RTT dall'output del ping
                output_lines = result.stdout.split("\n")
                for line in output_lines:
                    if "time=" in line:
                        time_index = line.find("time=")
                        time_str = line[time_index:].split(" ")[0]
                        time=time_str.split("time=")[1]
                        file.write(time+','+'0'+','+'0'+'\n')
                        print(f"Ping Test - {time_str}")
            else:
                print("Ping Test - Nessuna risposta dal server")
        except Exception as e:
            print(f"Errore nell'esecuzione del ping: {e}")
            

#Funzione di test echo che invia il messaggio "Messaggio di test" e attende la risposta da parte
#del server. Tale funzione avvia un timer esattamente prima dell'invio e lo arresta esattamente
#dopo aver ricevuto il messaggio. La differenza tra "end_time" e "start_time" costituisce il 
#valore RTT oggetto di questo test.
def echo_test(client_socket, file, traffic,ntp_client):
    """
    Esegue un test di echo inviando messaggi al server e ricevendo risposte.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
    """
    num_messages=100
    for _ in range(num_messages):
        file.write("echo"+','+str(traffic)+',')
        message = "Messaggio di test"
        rtt,response=send_recv_rtt(client_socket,message)
        file.write(str(rtt)+','+'0'+','+'0'+'\n')
        print(f"Echo Test - RTT: {rtt:.6f} s, Ricevuto: {response.decode()}")
        
#Funziozio di test che permette l'invio di messaggi TCP ad invervalli regolari, definiti
#attraverso l'array "interval" passato come argomento. Tale funzione avvia un timer esattamente 
#prima dell'invio e lo arresta esattamente dopo aver ricevuto il messaggio. La differenza tra 
#"end_time" e "start_time" costituisce il valore RTT oggetto di questo test.
def latency_interval_test(client_socket, interval, file, traffic):
    """
    Esegue un test di latenza calcolando il tempo di andata e ritorno di un messaggio TCP
    mandando messaggi ad intervalli regolari.

    Args:
        client_socket (socket): Socket connesso al server.
        interval array(str): Intervallo di tempo tra i messaggi in secondi.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
    """
    interval_list=interval[0].split(" ")
    print(interval_list)
    num_messages=50
    for inter in interval_list:
        for _ in range(num_messages):
            file.write("Intervallo: "+str(inter)+' s,'+str(traffic)+',')
            message = "Latency Test"
            rtt,response=send_recv_rtt(client_socket,message)
            file.write(str(rtt)+','+'0'+','+'0'+'\n')
            print(f"Latenza Test - RTT: {rtt:.6f} s, Ricevuto: {response.decode()}")
            inter_float=float(inter)
            if inter_float-rtt >= 0:
                time.sleep(inter_float-rtt)
                
#Funzione di test che permette l'invio di messaggi TCP con dimensioni del payload crescenti.
#Tale funzione avvia un timer esattamente prima dell'invio e lo arresta esattamente dopo aver
#ricevuto il messaggio. La differenza tra "end_time" e "start_time" costituisce il valore RTT 
#oggetto di questo test.
def payload_variation_test(client_socket, file, traffic, payload):
    """
    Esegue un test di variazione del payload inviando messaggi di dimensioni crescenti.

    Args:
        client_socket (socket): Socket connesso al server.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
        payload (list of str): dimensioni del payload
    """
    payload_list = payload[0].split(" ")
    print(payload_list)
    for _ in range(50):
        for payload_size in payload_list:
            payload_size_int = int(payload_size)
            file.write("Dim payload: "+payload_size+','+str(traffic)+',')
            message = "X" * payload_size_int
            rtt,response=send_recv_rtt(client_socket,message)
            print(f"Payload Test - Dimensione: {payload_size} bytes, RTT: {rtt:.6f} s, Ricevuto: {len(response)} bytes")
            file.write(str(rtt)+','+'0'+','+'0'+'\n')
            
#Funzione di test che permette l'invio di messaggi UDP. Tale funzione avvia un timer esattamente 
#prima dell'invio e lo arresta esattamente dopo aver ricevuto il messaggio. La differenza tra "end_time"
#e "start_time" costituisce il valore RTT oggetto di questo test.
def udp_test(host, port, file, traffic):
    """
    Esegue un test UDP inviando pacchetti al server e ricevendo risposte.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server UDP e' in ascolto.
        file (File): File .csv per il salvataggio dei dati
        traffic (str): scenario di traffico del test corrente 
    """
    num_messages=100
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "Messaggio di test UDP"
    for _ in range(num_messages):
        file.write("UDP,"+str(traffic)+",")
        start_time = time.time()
        udp_socket.sendto(message.encode(), (host, port))
        response, _ = udp_socket.recvfrom(65536)
        end_time = time.time()
        rtt=end_time-start_time
        file.write(str(rtt)+','+'0'+','+'0'+'\n')
        print(f"UDP Test - RTT: {rtt:.6f} s, Ricevuto: {response.decode()}")

    udp_socket.close()

#Funzione di test utilizzando il comando "traceroute"
def tracerout(host):
    result = subprocess.run(["sudo","traceroute","-I", "www.unibs.it"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        file=open("tracerouce.txt",'a')
        outputline=result.stdout
        print(outputline)
        file.write(outputline)
        
#Funzione principale di scelta della tipologia di test. All'avvio tale funzione apre un file che
#avra il nome: "istanti_temporali_"+data del giorno espressa come ANNO-MESE-GIORNO+".csv". Se il file risulta
#vuoto, allora scrive l'intestazione necessaria alla suddivisione del file csv. Nel caso contrario, procede alla
#selezione di test in cui si pone in attesa che l'utente fornisca un numero da 1 a 6 tramite l'input da tastiera.
#Alla fine di ogni test, per evitare problemi, la connessione verso il server viene interrotta, in modo da poterla
#ristabilire all'inizio di un nuovo test. Infatti, essendo la selezione all'interno di un "while TRUE:", al termine
#di un test, dopo aver chiuso le connessioni, il programma si riporta nello stato di selezione del test attendendo
#nuovamente l'input dall'utente.
#Il programma termina quando l'utente manda come input la scelta numero 7 che chiude il file .csv di salvataggio dei
#dati e termina l'esecuzione.
def run_test_cycle(host, tcp_port, udp_port, interval, traffic, payload):
    """
    Esegue un ciclo di test di rete per ciascun intervallo specificato.

    Args:
        host (str): Indirizzo IP del server.
        tcp_port (int): Porta del server TCP.
        udp_port (int): Porta del server UDP.
        intervals (list of float): Elenco degli intervalli tra i test in secondi.
        traffic (str): Scenario di traffico del test corrente
    """
    ntp_client =ntplib.NTPClient()
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("Tipo Test,Traffico,RTT,RTT_npt,OTT\n")
        print("File csv creato.")
    while True:
        print("\nSeleziona un test da eseguire:")
        print("1. Echo Test")
        print("2. Ping Test")
        print("3. Latency Test")
        print("4. Payload Variation Test")
        print("5. UDP Test")
        print(f"6. Traceroute verso {host}")
        print("7. Test sfruttando server ntp")
        print("8. Esci")

        scelta = input("Inserisci il numero del test da eseguire: ")

        if scelta == '1':
            print("\nEsecuzione Echo Test:")
            client_socket = connect_to_server(host, tcp_port)
            try:
                echo_test(client_socket, file, traffic,ntp_client)
            finally:
                client_socket.close()
                print("Connessione al server chiusa dopo l'echo test")

        elif scelta == '2':
            print("\nEsecuzione Ping Test:")
            ping_test_subprocess(host, file, traffic)

        elif scelta == '3':
            print("\nEsecuzione Latency Test:")
            client_socket = connect_to_server(host, tcp_port)
            try:
                latency_interval_test(client_socket, interval, file, traffic)
            finally:
                client_socket.close()
                print("Connessione al server chiusa dopo il test di latenza")

        elif scelta == '4':
            print("\nEsecuzione Payload Variation Test:")
            client_socket = connect_to_server(host, tcp_port)
            try:
                payload_variation_test(client_socket, file, traffic, payload)
            finally:
                client_socket.close()
                print("Connessione al server chiusa dopo il test di variazione del payload")

        elif scelta == '5':
            print("\nEsecuzione UDP Test:")
            udp_test(host, udp_port, file, traffic)
        elif scelta == '6':
            print(f"\nEsecuzione del comando traceroute verso {host}")
            tracerout(host)
        elif scelta == '7':
            print("Test echo con orologi da Server NTP.") 
            client_socket = connect_to_server(host, tcp_port)
            ntest = 1000
            for _ in range(ntest):
                rtt,ott = test_ntp(client_socket,ntp_client,host,tcp_port) 
                file.write("NTP"+','+str(traffic)+','+'0'+','+str(rtt)+','+str(ott)+'\n')
                time.sleep(0.5)
        elif scelta == '8':
            file.close()
            print("Uscita dal programma.")
            break

        else:
            print("Selezione non valida. Per favore, riprova.")
            
#Funzione principale che all'avvio del programma tramite l'oggetto "parser" consente di eseguire il codice
#specificando gli argomenti necessari alla realizzazione del test. Dopo aver aggiunto tutti gli argomenti
#passati al lancio del programma python, viene eseguita la funzione "run_test_cycle" e si entra nella fase
#di test. 
if __name__ == "__main__":
    """
        server_host: Indirizzo IP del server
        tcp_port: Porta del server TCP
        udp_port: Porta del server UDP
        intervals: Intervalli di tempo tra i messaggi
        traffic: Scenario di traffico del test
        payload: Dimensioni crescenti del payload per test
    
    """
    parser = argparse.ArgumentParser(description='Client TCP e UDP per il test della connessione.')
    parser.add_argument('--server_host', type=str, required=True, help='Indirizzo IP del server')
    parser.add_argument('--tcp_port', type=int, required=True, help='Porta del server TCP')
    parser.add_argument('--udp_port', type=int, required=True, help='Porta del server UDP')
    parser.add_argument('--interval', nargs='+', required=True, help='Intervalli di tempo tra i messaggi')
    parser.add_argument('--traffic', type=str, required=True, help="Scenario di traffico del test")
    parser.add_argument('--payload', nargs='+', required=True, help='Dimensioni di payload')
    args = parser.parse_args()

    run_test_cycle(args.server_host, args.tcp_port, args.udp_port, args.interval, args.traffic, args.payload)
