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
IPERF_CLIENT_BITRATE=$(ini_get_value iperf bit_rate) #bit rate di trasferimento che il client cercherà di raggiungere
IPERF_CLIENT_MULTI=$(ini_get_value iperf parallel) #numero di stream in parallelo
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia) #interfaccia sui cui si mette in ascolto wireshark
WIRESHARK_DURATA=$(ini_get_value wireshark durata) #durata dell'ascolto tramite wireshark
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file) #file di output generato dall'ascolto di wireshark
IP_SERVER=$(ini_get_value server ip) #indirizzo IP del SERVER realizzato per i test di connessione
FILE_CSV_WIRESHARK=$(ini_get_value wireshark out_csv) #file .csv in cui vengono salvati i valori ottenuti da wireshark 

#_____________________________________________________________________________________________________________________
#Avvio del Client IPERF & del Client che manderà messaggi al server di echo variando la dimensione del payload dei pacchetti:
TRAFFICO_IPERF=("1Mbits" "100Mbits" "1Gbits" "9Gbits")
#DIM_PAYLOAD=("8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" "16384")
DIM_PAYLOAD=("0" "0" "0" "0" "0" "0" "0" "0" "0" "0" "0" "0")
for test in "${TRAFFICO_IPERF[@]}"
    do
    start_iperf_client $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_CLIENT_DURATION $IPERF_CLIENT_BITRATE 
    pid_iperf=$!
    for dim in "${DIM_PAYLOAD[@]}"
        do
        python3 Client.py --server_host "$IP_SERVER" --server_port "$IPERF_SERVER_PORT" --payload_size "$dim" &
    done
    wait $pid_iperf
done

