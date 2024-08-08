import socket
import Utility
import time
import argparse
import subprocess

from datetime import datetime
from ping3 import ping
PAYLOAD=[8,16,32,64,128,256,512,1024,1500]

def connect_to_server(host, port):
    """
    Crea e stabilisce una connessione TCP con il server specificato.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server è in ascolto.

    Returns:
        socket: Oggetto socket connesso al server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connesso al server {host}:{port}")
    return client_socket


def ping_test_subprocess(host, file, traffic):
    """
    Esegue un test di ping al server utilizzando subprocess per aggirare i problemi di permessi.

    Args:
        host (str): Indirizzo IP del server.
        num_pings (int): Numero di ping da inviare.
    """
    num_pings=5
    print(f"Eseguendo ping verso {host} utilizzando subprocess...")
    for _ in range(num_pings):
        file.write("ping3"+','+str(traffic)+',')
        try:
            result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                # Estrarre l'RTT dall'output del ping
                output_lines = result.stdout.split("\n")
                for line in output_lines:
                    if "time=" in line:
                        time_index = line.find("time=")
                        time_str = line[time_index:].split(" ")[0]
                        file.write(time_str+'\n')
                        print(f"Ping Test - {time_str}")
            else:
                print("Ping Test - Nessuna risposta dal server")
        except Exception as e:
            print(f"Errore nell'esecuzione del ping: {e}")

def send_precise(sock, data):
    """
    Invia i dati attraverso il socket in modo preciso, assicurando l'invio completo.

    Args:
        sock (socket): Il socket attraverso il quale inviare i dati.
        data (bytes): I dati da inviare.
    """
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Il socket è stato chiuso dall'altro lato")
        total_sent += sent

def echo_test(client_socket, file, traffic):
    """
    Esegue un test di echo inviando messaggi al server e ricevendo risposte.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    num_messages=100
    for _ in range(num_messages):
        file.write("echo"+','+str(traffic)+',')
        message = "Test message"
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(1024)
        end_time = time.time()
        rtt=end_time-start_time
        file.write(str(rtt)+'\n')
        print(f"Echo Test - RTT: {rtt:.6f} s, Ricevuto: {response.decode()}")


def latency_test(client_socket, interval, file, traffic):
    """
    Esegue un test di latenza calcolando il tempo di andata e ritorno di un messaggio TCP.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    num_messages=10
    for _ in range(num_messages):
        file.write(str(interval)+','+str(traffic)+',')
        message = "Latency Test"
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(1500)
        end_time = time.time()
        rtt = end_time-start_time
        file.write(str(rtt)+'\n')
        print(f"Latenza Test - RTT: {rtt:.6f} s, Ricevuto: {response.decode()}")

def payload_variation_test(client_socket, file, traffic):
    """
    Esegue un test di variazione del payload inviando messaggi di dimensioni crescenti.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        max_payload_size (int): Dimensione massima del payload in byte.
        step_size (int): Incremento della dimensione del payload ad ogni ciclo.
    """
    max_payload_size=1500
    payload_size = 8  # Dimensione iniziale del payload
    while payload_size <= max_payload_size:
        file.write(payload_size+','+str(traffic)+',')
        message = "X" * payload_size
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(1500)
        end_time = time.time()
        rtt=start_time-end_time
        print(f"Payload Test - Dimensione: {payload_size} bytes, RTT: {rtt:.6f} s, Ricevuto: {len(response)} bytes")
        file.write(str(rtt)+'\n')
        payload_size = payload_size*2

def udp_test(host, port, file, traffic):
    """
    Esegue un test UDP inviando pacchetti al server e ricevendo risposte.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server UDP è in ascolto.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    num_messages=50
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "UDP Test message"
    for _ in range(num_messages):
        file.write("UDP,"+str(traffic)+",")
        start_time = time.time()
        udp_socket.sendto(message.encode(), (host, port))
        response, _ = udp_socket.recvfrom(2048)
        end_time = time.time()
        rtt=end_time-start_time
        file.write(str(rtt)+'\n')
        print(f"UDP Test - RTT: {end_time - start_time:.6f} s, Ricevuto: {response.decode()}")

    udp_socket.close()

def run_test_cycle(host, tcp_port, udp_port, intervals, traffic):
    """
    Esegue un ciclo di test di rete per ciascun intervallo specificato.

    Args:
        host (str): Indirizzo IP del server.
        tcp_port (int): Porta del server TCP.
        udp_port (int): Porta del server UDP.
        intervals (list of float): Elenco degli intervalli tra i test in secondi.
    """
    
    data_corrente = datetime.now()
    data_stringa = data_corrente.strftime("%Y-%m-%d")
    filecsv="istanti_temporali_"+data_stringa+".csv"
    file=open(filecsv,"a")
    if file.tell()==0:
        file.write("Tipo Test,Traffico,RTT\n")
        print("File csv creato.")
    while True:
        print("\nSeleziona un test da eseguire:")
        print("1. Echo Test")
        print("2. Ping Test")
        print("3. Latency Test")
        print("4. Payload Variation Test")
        print("5. UDP Test")
        print("6. Esci")

        scelta = input("Inserisci il numero del test da eseguire: ")

        if scelta == '1':
            print("\nEsecuzione Echo Test:")
            for interval in intervals:
                print(f"\nAvvio del ciclo di test con intervallo: {interval} secondi")
                client_socket = connect_to_server(host, tcp_port)
                try:
                    echo_test(client_socket, file, traffic)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo l'echo test")

        elif scelta == '2':
            print("\nEsecuzione Ping Test:")
            ping_test_subprocess(host, file, traffic)

        elif scelta == '3':
            print("\nEsecuzione Latency Test:")
            for interval in intervals:
                print(f"\nAvvio del ciclo di test con intervallo: {interval} secondi")
                client_socket = connect_to_server(host, tcp_port)
                try:
                    latency_test(client_socket, interval, file, traffic)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo il test di latenza")

        elif scelta == '4':
            print("\nEsecuzione Payload Variation Test:")
            for interval in intervals:
                print(f"\nAvvio del ciclo di test con intervallo: {interval} secondi")
                client_socket = connect_to_server(host, tcp_port)
                try:
                    payload_variation_test(client_socket, interval, file)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo il test di variazione del payload")

        elif scelta == '5':
            print("\nEsecuzione UDP Test:")
            udp_test(host, udp_port, file, traffic)

        elif scelta == '6':
            file.close()
            print("Uscita dal programma.")
            break

        else:
            print("Selezione non valida. Per favore, riprova.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client TCP e UDP per il test della connessione.')
    parser.add_argument('--server_host', type=str, required=True, help='Indirizzo IP del server')
    parser.add_argument('--tcp_port', type=int, required=True, help='Porta del server TCP')
    parser.add_argument('--udp_port', type=int, required=True, help='Porta del server UDP')
    parser.add_argument('--intervals', nargs='+', type=float, required=True, help='Intervalli di tempo tra i messaggi')
    parser.add_argument('--traffic', type=str, required=True, help="Scenario di traffico del test")
    args = parser.parse_args()

    run_test_cycle(args.server_host, args.tcp_port, args.udp_port, args.intervals, args.traffic)
