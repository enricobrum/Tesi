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
 
    while True: 
        file=open("Istanti_Temporali_SERVER_UDP.txt","a")
        data, address = sock.recvfrom(data_payload) 
        file.write("Ricevuto: \n")
        time=str(datetime.now().time().second)+"s"+str(datetime.now().time().microsecond)+"us"
        file.write(time)
        file.write("\n")
        if data: 
            sent = sock.sendto(data, address) 
            time=str(datetime.now().time().second)+"s"+str(datetime.now().time().microsecond)+"us"
            file.write("Inoltrato: \n")
            file.write(time)
            file.write("\n")
            print ("sent %s bytes back to %s" % (sent, address)) 
        file.close()
 
if __name__ == '__main__': 
    echo_server(9900) 