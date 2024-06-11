#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 1
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import socket
import sys
import argparse
import time
from time import ctime
from datetime import datetime


host = 'localhost'
data_payload = 2048

def echo_client(port):
    """ A simple echo client """
    # Create a UDP socket
    file=open("Istanti_Temporali_CLIENT_UDP.csv","a")
    file.write("InviatoCLIENT;")
    file.write("RicevutoCLIENT;\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    print ("Connecting to %s port %s" % server_address)
    message = 'This is the message.  It will be repeated.'
    for i in range(10):
        # Send data
        message = "Test message. This will be echoed"
        now=datetime.now().time()
        secondi=now.second
        micros=now.microsecond 
        file.write(str(secondi)+'.'+str(micros)+";")
        sent = sock.sendto(message.encode('utf-8'), server_address)
            # Receive response
        data, server = sock.recvfrom(data_payload)
        now=datetime.now().time()
        secondi=now.second
        micros=now.microsecond 
        file.write(str(secondi)+'.'+str(micros)+";")
        file.write("\n")
        print ("received %s" % data)
    esc="ESC"
    sock.sendto(esc.encode(),server_address)

    print ("Closing connection to the server")
    sock.close()
    file.close()


if __name__ == '__main__':
    echo_client(9900)