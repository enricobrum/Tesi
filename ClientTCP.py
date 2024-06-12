import socket
import sys
import Utility
#_______________________________________________________________________
#FUNZIONE: RICHIESTA DA CLIENT --> SERVER
def richieste(s,n_test):
    file=open("Istanti_client_tcp.csv","a")
    file.write("Inviato;Ricevuto;\n")
    msg="Messaggio di test"
    for i in range(n_test):
        sec1,us1=Utility.time_stamp()
        s.send(msg.encode('utf-8'))
        data=s.recv(4096)
        sec2,us2=Utility.time_stamp()
        file.write(str(sec1)+'.'+str(us1)+';')
        file.write(str(sec2)+'.'+str(us2)+';')
        file.write("\n")
    file.close()
#______________________________________________________________
#FUNZIONE: CLIENT TCP
def client_tcp(server_addr,n_test):
    try:
        s=socket.socket()
        s.connect(server_addr)
    except socket.error as errore:
        sys.exit()
    richieste(s,n_test)