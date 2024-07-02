#!/bin/bash
#Programma utilizzato per l'avvio dei server da lato core 5G posti sul nodo centrale della rete 5G Firecell. Inoltre è anche configurato
#l'applicazione wireshark al fine di ottenere i valori dei time-stamp relativi ai pacchetti scambiati nella fase di test della rete.
#______________________________________________________________________________________________________________________________________
#Importo i file contenenti le funzioni utilizzate per avviare e controllare i Client e 
#server, la lettura del file di configurazione, la configurazione di client e server iperf e 
#la configurazione dell'ascolto effettuato da wireshark.
chmod +x Lettura_File_Config.sh 
chmod +x Iperf.sh
chmod +x Wireshark.sh
chmod +x Analisi_Pacchetti.sh
source Lettura_File_Config.sh #Lettura del file di configurazione contenenti i valori utilizzati per i test
. Iperf.sh #Funzioni per l'avvio di server il client iperf
. Wireshark.sh #Funzione per l'avvio dell'ascolto su wireshark
#______________________________________________________________________________________________________________________________________
IP_SERVER=$(ini_get_value server ip) #indirizzo IP del server di echo
PORT_SERVER=$(ini_get_value server port) #port in cui si pone in ascolto il server di echo
IPERF_SERVER_IP=$(ini_get_value iperf ip_server) #indirizzo IP del server iperf
IPERF_SERVER_PORT=$(ini_get_value iperf server_port) #porta su cui il server si pone in ascolto
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia)
WIRESHARK_DURATA=$(ini_get_value wireshark durata)
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file)
FILE_CSV_WIRESHARK=$(ini_get_value wireshark out_csv)
#_____________________________________________________________________________________________________________________________________
python3 Server.py --host "$IP_SERVER" --port "$PORT_SERVER" & #avvio del server con i parametri ottenuti da file di configurazione
start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT & #avvia il server iperf
avvio_tshark $WIRESHARK_INTERFACCIA $WIRESHARK_DURATA $WIRESHARK_OUTPUT_FILE 
wait $!
if [ $? -eq 0 ]; then
    echo "Cattura completata. File salvato in $WIRESHARK_OUTPUT_FILE"
    # Avvia Wireshark per analizzare il file di cattura
    wireshark $WIRESHARK_OUTPUT_FILE &
    kill $!
else
    echo "Errore nella cattura dei pacchetti."
    exit 1
fi
# Terminare il server iperf
kill $PID
echo "Server iperf terminato."

./Analisi_Pacchetti.sh "$WIRESHARK_OUTPUT_FILE" "$IP_SERVER" "$FILE_CSV_WIRESHARK"


