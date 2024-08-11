#!/bin/bash
#Programma utilizzato per l'avvio dei server da lato core 5G posti 
#sul nodo centrale della rete 5G Firecell. Inoltre e' anche configurato
#l'applicazione wireshark al fine di ottenere i valori dei time-stamp 
#relativi ai pacchetti scambiati nella fase di test della rete.
#_______________________________________________________________________________
#Importo i file contenenti le funzioni utilizzate per avviare e controllare
#i Client e server, la lettura del file di configurazione,
#la configurazione di client e server iperf e la configurazione dell'ascolto
#effettuato da wireshark.
chmod +x Lettura_File_Config.sh 
chmod +x Iperf.sh
source Lettura_File_Config.sh #Lettura del file di configurazione contenenti
                              #i valori utilizzati per i test
source Iperf.sh
#_______________________________________________________________________________
PORT_SERVER=$(ini_get_value server port) #port in cui si pone il server di echo
IPERF_SERVER_IP=$(ini_get_value iperf ip_server) #indirizzo IP del server iperf
IPERF_SERVER_PORT=$(ini_get_value iperf server_port) #porta su cui il server si 
                                                     #pone in ascolto

#_________________________________________________________________________________
start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT #avvia il server iperf

