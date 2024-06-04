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
    file=open("Istanti_Temporali_CLIENT.txt","a")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    print ("Connecting to %s port %s" % server_address)
    message = 'This is the message.  It will be repeated.'

    try:

        # Send data
        message = "Test message. This will be echoed"
        print ("Sending %s" % message)
        print(datetime.now().time())
        file.write("Invio: \n")
        file.write(str(datetime.now().time()))
        file.write("\n")
        sent = sock.sendto(message.encode('utf-8'), server_address)

        # Receive response
        data, server = sock.recvfrom(data_payload)
        print(datetime.now().time())
        file.write("Ricezione: \n")
        file.write(str(datetime.now().time()))
        file.write("\n")
        print ("received %s" % data)

    finally:
        print ("Closing connection to the server")
        sock.close()
        file.close()

if __name__ == '__main__':
    echo_client(9900)