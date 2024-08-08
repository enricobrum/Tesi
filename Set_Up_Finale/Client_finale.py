import socket
import time
import argparse
from ping3 import ping

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

def echo_test(client_socket, interval, num_messages=10):
    """
    Esegue un test di echo inviando messaggi al server e ricevendo risposte.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    for _ in range(num_messages):
        message = "Test message"
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(1024)
        end_time = time.time()
        print(f"Echo Test - RTT: {end_time - start_time:.6f} s, Ricevuto: {response.decode()}")
        time.sleep(interval)

def ping_test(host, num_pings=5):
    """
    Esegue un test di ping al server per misurare la latenza ICMP.

    Args:
        host (str): Indirizzo IP del server.
        num_pings (int): Numero di ping da inviare.

    """
    print(f"Eseguendo ping verso {host}...")
    for _ in range(num_pings):
        delay = ping(host)
        if delay is not None:
            print(f"Ping Test - RTT: {delay:.6f} s")
        else:
            print("Ping Test - Nessuna risposta dal server")

def latency_test(client_socket, interval, num_messages=10):
    """
    Esegue un test di latenza calcolando il tempo di andata e ritorno di un messaggio TCP.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    for _ in range(num_messages):
        message = "Latency Test"
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(1024)
        end_time = time.time()
        print(f"Latenza Test - RTT: {end_time - start_time:.6f} s, Ricevuto: {response.decode()}")
        time.sleep(interval)

def payload_variation_test(client_socket, interval, max_payload_size=1500, step_size=100):
    """
    Esegue un test di variazione del payload inviando messaggi di dimensioni crescenti.

    Args:
        client_socket (socket): Socket connesso al server.
        interval (float): Intervallo di tempo tra i messaggi in secondi.
        max_payload_size (int): Dimensione massima del payload in byte.
        step_size (int): Incremento della dimensione del payload ad ogni ciclo.
    """
    payload_size = 100  # Dimensione iniziale del payload
    while payload_size <= max_payload_size:
        message = "X" * payload_size
        start_time = time.time()
        send_precise(client_socket, message.encode())
        response = client_socket.recv(2048)
        end_time = time.time()
        print(f"Payload Test - Dimensione: {payload_size} bytes, RTT: {end_time - start_time:.6f} s, Ricevuto: {len(response)} bytes")
        payload_size += step_size
        time.sleep(interval)

def udp_test(host, port, num_messages=10):
    """
    Esegue un test UDP inviando pacchetti al server e ricevendo risposte.

    Args:
        host (str): Indirizzo IP del server.
        port (int): Porta su cui il server UDP è in ascolto.
        num_messages (int): Numero di messaggi da inviare nel ciclo.
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "UDP Test message"
    for _ in range(num_messages):
        start_time = time.time()
        udp_socket.sendto(message.encode(), (host, port))
        response, _ = udp_socket.recvfrom(2048)
        end_time = time.time()
        print(f"UDP Test - RTT: {end_time - start_time:.6f} s, Ricevuto: {response.decode()}")
    udp_socket.close()

def run_test_cycle(host, tcp_port, udp_port, intervals):
    """
    Esegue un ciclo di test di rete per ciascun intervallo specificato.

    Args:
        host (str): Indirizzo IP del server.
        tcp_port (int): Porta del server TCP.
        udp_port (int): Porta del server UDP.
        intervals (list of float): Elenco degli intervalli tra i test in secondi.
    """
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
                    echo_test(client_socket, interval)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo l'echo test")

        elif scelta == '2':
            print("\nEsecuzione Ping Test:")
            ping_test(host)

        elif scelta == '3':
            print("\nEsecuzione Latency Test:")
            for interval in intervals:
                print(f"\nAvvio del ciclo di test con intervallo: {interval} secondi")
                client_socket = connect_to_server(host, tcp_port)
                try:
                    latency_test(client_socket, interval)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo il test di latenza")

        elif scelta == '4':
            print("\nEsecuzione Payload Variation Test:")
            for interval in intervals:
                print(f"\nAvvio del ciclo di test con intervallo: {interval} secondi")
                client_socket = connect_to_server(host, tcp_port)
                try:
                    payload_variation_test(client_socket, interval)
                finally:
                    client_socket.close()
                    print("Connessione al server chiusa dopo il test di variazione del payload")

        elif scelta == '5':
            print("\nEsecuzione UDP Test:")
            udp_test(host, udp_port)

        elif scelta == '6':
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

    args = parser.parse_args()

    run_test_cycle(args.server_host, args.tcp_port, args.udp_port, args.intervals)
