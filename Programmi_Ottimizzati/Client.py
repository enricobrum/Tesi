#Programma Python per la realizzazione di un Client sfruttando il protocollo TCP.
#Questo client ha la funzione di inviare verso il server specificato dai parametri,
#un messaggio contenente il payload generato dalla dimensione passata tramite parametro.
#Una volta inviato, tale Client si pone in attesa di una risposta dal server che sarà
#realizzato in modo da emettere un echo del messaggio. 
import socket
import argparse
import Utility

def tcp_client(server_host,server_port,payload_size):
    file=open("Istanti_temportali.csv","a")
    file.write("Inviato;Ricevuto;\n")
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host,server_port))
            print(f"Connessione al server TCP {server_host}:{server_port}")
            payload=b'a'*payload_size
            sec1,us1=Utility.time_stamp()
            client_socket.sendall(payload)
            print(f"Inviati {payload_size} bytes")
            data=client_socket.recv(65536) #buffer impostato al massimo in modo da effettuare test con variazione del payload
            sec2,us2=Utility.time_stamp()
            file.write(str(sec1)+'.'+str(us1)+';')
            file.write(str(sec2)+'.'+str(us2)+';')
            file.write("\n")
            print(f"Ricevuto {len(data)} bytes da {server_host}:{server_port}")
            file.close()
    except Exception as e:
        print(f"Eccezione {e} durante la connessione con il server.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client")
    parser.add_argument('--server_host', default='127.0.0.1', help='Server host')
    parser.add_argument('--server_port', type=int, default=12345, help='Server port')
    parser.add_argument('--payload_size', type=int, default=1024, help='Payload size in bytes')
    args = parser.parse_args()

    tcp_client(args.server_host, args.server_port, args.payload_size)
       