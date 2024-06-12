import socket

#FUNZIONE: RICEZIONE DATI DA CLIENT
def ricevi_dati(conn):
    while True:
        richiesta=conn.recv(4096) #riceve i dati contenenti nel buffer dati a 4096
        conn.send(richiesta.encode())
        if richiesta=='ESC': break

#FUNZIONE: SERVER TCP
def sub_server(indirizzo,backlog=1):
    try:
        s=socket.socket()
        s.bind(indirizzo)
        s.listen(backlog)
        print("Server inizializzato. In ascolto...\n")
    except socket.error as errore:
        print(f"Qualcosa è andato storto...\n{errore}")
        print("Reinizializzazione...\n")
        sub_server(indirizzo,backlog=1)
    conn,indirizzo_client=s.accept() #Instaurazione connessione con il client
    print(f"Connessione stabilità con l'indirizzo:{indirizzo_client}")
    ricevi_dati(conn)
    
#__________________________________________________________________________________________
if __name__=='__main__':
    sub_server(("",20000))