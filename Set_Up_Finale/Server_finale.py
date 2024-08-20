import socket
import threading
import argparse

#Funzione per la gestione della connessione TCP
def handle_tcp_connection(client_socket, client_address):
    """
    Gestisce una connessione TCP con il client.

    Args:
        client_socket (socket): Il socket connesso al client.
        client_address (tuple): L'indirizzo del client.
    """
    print(f"TCP Connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(65536)
            if not data:
                break
            client_socket.sendall(data)
    except Exception as e:
        print(f"Errore nella connessione TCP: {e}")
    finally:
        client_socket.close()
        print(f"Connessione TCP chiusa con: {client_address}")
        
#Funzione per l'avvio del server TCP sull'indirizzo IP e porta passati come 
#argomenti, rispettivamente, host e port
def tcp_server(host, port):
    """
    Avvia un server TCP.

    Args:
        host (str): Indirizzo IP su cui il server e' in ascolto.
        port (int): Porta su cui il server e' in ascolto.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server TCP in ascolto su {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_tcp_connection, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("\nArresto del server TCP.")
    finally:
        server_socket.close()

#Funzione per l'avvio del server UDP sull'indirizzo IP e porta passati come 
#argomenti, rispettivamente, host e port
def udp_server(host, port):
    """
    Avvia un server UDP.

    Args:
        host (str): Indirizzo IP su cui il server e' in ascolto.
        port (int): Porta su cui il server e' in ascolto.
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    print(f"Server UDP in ascolto su {host}:{port}")

    try:
        while True:
            data, client_address = udp_socket.recvfrom(65536)
            print(f"Ricevuto messaggio da {client_address}: {data.decode()}")
            udp_socket.sendto(data, client_address)
    except KeyboardInterrupt:
        print("\nArresto del server UDP.")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client TCP e UDP per il test della connessione.')
    parser.add_argument('--server_host', type=str, required=True, help='Indirizzo IP del server')
    parser.add_argument('--tcp_port', type=int, required=True, help='Porta del server TCP')
    parser.add_argument('--udp_port', type=int, required=True, help='Porta del server UDP')

    args = parser.parse_args()

    threading.Thread(target=tcp_server, args=(args.server_host, args.tcp_port)).start()
    threading.Thread(target=udp_server, args=(args.server_host, args.udp_port)).start()
