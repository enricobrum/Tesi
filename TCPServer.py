# Creazione CLIENT SOCKET:
#--------------------------------
# 1 - Creazione socket                      # socket.socket()
# 2 - Connessione al Server                 # connect(indirizzo)
# 3 - Invio di una Richiesta al Server      # send()
# 4 - Ricezione della Risposta dal Server   # recv()
# Creazione SERVER SOCKET:
#--------------------------------
# 1 - Creazione socket                                                              # socket.socket()
# 2 - Collegamento del socket all'indirizzo della macchina e alla Porta Designata   # bind()
# 3 - Messa in ascolto in attesa della connessione del Client                       # listen()
# 4 - Accettazione del Client                                                       # accept()
# 5 - Ricezione Richiesta dal Client                                                # recv()
# 4 - Elaborazione di una Risposta                                                  # subprocess()
# 5 - Invio Risposta al Client       
import socket
import subprocess

def ricevi_comandi(conn):
    while True:
        richiesta = conn.recv(4096)
        risposta = richiesta
        conn.send(risposta)
        
def sub_server(indirizzo,backlog=1):
    try:
        s=socket.socket()
        s.bind(indirizzo)
        s.listen(backlog)
        print("server inizializzato, ora in ascolto...")
    except socket.error as errore:
        print(f"qualcosa è andato storto.. \n{errore}")
        print("sto tentato di rienizializzare il server..")
        sub_server(indirizzo,backlog=1)
    conn,indirizzo_client=s.accept()
    print(f"connessione server - client stabilita:{indirizzo_client}")
    ricevi_comandi(conn)
    
if __name__ == '__main__':
    sub_server(("127.0.0.1",20000))