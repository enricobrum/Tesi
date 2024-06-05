import requests
import time
from time import ctime
from datetime import datetime

port = 80 # Port to listen on (non-privileged ports are > 1023)

    # dizionario: 
hosts_to_test = {
    'http://google.com' : 80,
    'http://127.0.0.1' : 8080,
    'http://unibs.it' : 80
}

    # Iterate the Serevrs/Hosts list
for hostname in hosts_to_test.keys():
    port = hosts_to_test[hostname]
    print(datetime.now().time().microsecond)
    response = requests.get(hostname+":"+str(port))
    print(datetime.now().time().microsecond)
    print("risposta:",response.url)
        

