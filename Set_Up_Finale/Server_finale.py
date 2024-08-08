import socket
import threading

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
            data = client_socket.recv(2048)
            if not data:
                break
            client_socket.sendall(data)
    except Exception as e:
        print(f"Errore nella connessione TCP: {e}")
    finally:
        client_socket.close()
        print(f"TCP Connection closed with {client_address}")

def tcp_server(host, port):
    """
    Avvia un server TCP.

    Args:
        host (str): Indirizzo IP su cui il server è in ascolto.
        port (int): Porta su cui il server è in ascolto.
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

def udp_server(host, port):
    """
    Avvia un server UDP.

    Args:
        host (str): Indirizzo IP su cui il server è in ascolto.
        port (int): Porta su cui il server è in ascolto.
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    print(f"Server UDP in ascolto su {host}:{port}")

    try:
        while True:
            data, client_address = udp_socket.recvfrom(2048)
            print(f"Ricevuto messaggio da {client_address}: {data.decode()}")
            udp_socket.sendto(data, client_address)
    except KeyboardInterrupt:
        print("\nArresto del server UDP.")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    tcp_port = 8080
    udp_port = 8081

    threading.Thread(target=tcp_server, args=(host, tcp_port)).start()
    threading.Thread(target=udp_server, args=(host, udp_port)).start()
