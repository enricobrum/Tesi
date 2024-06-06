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
file=open("Istanti_Temporali_HTTP.csv","a")
file.write("Invio;")
file.write("Risposta;\n")
for hostname in hosts_to_test.keys():
    port = hosts_to_test[hostname]
    now=datetime.now().time()
    secondi=now.second
    micros=now.microsecond 
    file.write(str(secondi)+'.'+str(micros)+";")
    response = requests.get(hostname+":"+str(port))
    now=datetime.now().time()
    secondi=now.second
    micros=now.microsecond 
    file.write(str(secondi)+'.'+str(micros)+";")
    file.write("\n")
    print("risposta:",response.url)
file.close()
        

