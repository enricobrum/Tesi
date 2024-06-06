import requests
import time
from time import ctime
from datetime import datetime

    # dizionario: 
hosts_to_test = {
    'http://google.com' : 80,
    'http://127.0.0.1' : 8080,
    'http://unibs.it' : 80
}

    # Iterate the Serevrs/Hosts list
file=open("Istanti_Temporali_HTTP.txt","a")
for hostname in hosts_to_test.keys():
    port = hosts_to_test[hostname]
    file.write("Invio richiesta:\n")
    now=datetime.now().time()
    time=str(now.second)+"s"+str(now.microsecond)+"us"
    file.write(time)
    response = requests.get(hostname+":"+str(port))
    now=datetime.now().time()
    time=str(now.second)+"s"+str(now.microsecond)+"us"
    file.write("\nRisposta:\n")
    file.write(time)
    file.write("\n")
    print("risposta:",response.url)
file.close()
        

