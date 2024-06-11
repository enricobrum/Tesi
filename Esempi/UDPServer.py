import socket 
import sys 
import argparse 

from time import ctime
from datetime import datetime


host = 'localhost' 
data_payload = 2048 

def echo_server(port):    
    """ A simple echo server """ 
    # Create a UDP socket 
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
 
    # Bind the socket to the port 
    server_address = (host, port) 
    print("Starting up echo server on %s port %s" % server_address) 
    
    sock.bind(server_address) 
    file=open("Istanti_Temporali_SERVER_UDP.csv","a")
    file.write("RicevutoSERVER;")
    file.write("InviatoSERVER;\n")    
    while True:
        data, address = sock.recvfrom(data_payload) 
        now=datetime.now().time()
        secondi=now.second
        micros=now.microsecond 
        file.write(str(secondi)+'.'+str(micros)+";")
        if data: 
            sent = sock.sendto(data, address) 
            now=datetime.now().time()
            secondi=now.second
            micros=now.microsecond 
            file.write(str(secondi)+'.'+str(micros)+";")
            file.write("\n")
            print ("sent %s bytes back to %s" % (sent, address))
        if data.decode() == 'ESC': break
    file.close()
    sock.close()

 
if __name__ == '__main__': 
    echo_server(9900) 