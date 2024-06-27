#!/bin/bash
#Importo i file contenenti le funzioni utilizzate per avviare e controllare i Client e 
#server, la lettura del file di configurazione, la configurazione di client e server iperf e 
#la configurazione dell'ascolto effettuato da wireshark.
chmod +x Lettura_File_Config.sh 
chmod +x Iperf.sh
chmod +x Wireshark.sh
source Lettura_File_Config.sh #Lettura del file di configurazione contenenti i valori utilizzati per i test
. Iperf.sh #Funzioni per l'avvio di server il client iperf
. Wireshark.sh #Funzione per l'avvio dell'ascolto su wireshark
#_____________________________________________________________________________________________________________________
#Costanti di lavoro ricavate dal file di configurazione:
IPERF_SERVER_IP=$(ini_get_value iperf ip_server) #indirizzo IP del server iperf
IPERF_SERVER_PORT=$(ini_get_value iperf server_port) #porta su cui il server si pone in ascolto
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration) #durata della comunicazione tra client e server iperf
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port) #porta in cui si pone in comunicazione il clientù
IPERF_CLIENT_PACK_SIZE=$(ini_get_value iperf packet_size) #dimensione dei pacchetti mandati nel traffico generato
IPERF_CLIENT_MULTI=$(ini_get_value iperf parallel) #numero di stream in parallelo
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia) #interfaccia sui cui si mette in ascolto wireshark
WIRESHARK_DURATA=$(ini_get_value wireshark durata) #durata dell'ascolto tramite wireshark
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file) #file di output generato dall'ascolto di wireshark
IP_SERVER=$(ini_get_value server ip) #indirizzo IP del SERVER realizzato per i test di connessione
FILE_CSV_WIRESHARK=$(ini_get_value wireshark out_csv) #file .csv in cui vengono salvati i valori ottenuti da wireshark 
#_____________________________________________________________________________________________________________________
#Avvio del server IPERF:
bash -c "start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT"
PID_SERVER_PORT=$!
sleep 5
#_____________________________________________________________________________________________________________________
