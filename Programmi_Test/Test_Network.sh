#!/bin/bash
source Lettura_File_Config.sh
source Iperf.sh
source Wireshark.sh
#___________________________________________________________
#Costanti ottenute tramite il file di configuraazione
IPERF_SERVER_IP=$(ini_get_value iperf ip)
IPERF_SERVER_PORT=$(ini_get_value iperf server_port)
IPERF_SERVER_OUTPUT_FILE=$(ini_get_value iperf output_file)
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration)
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port)
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia)
WIRESHARK_DURATA=$(ini_get_value wireshark durata)
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file)
#____________________________________________________________
start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT
sleep 5
avvio_tshark $WIRESHARK_INTERFACCIA $WIRESHARK_DURATA $WIRESHARK_OUTPUT_FILE
start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $IPERF_CLIENT_DURATION

# Controlla se la cattura è stata completata con successo
    echo "Cattura completata. File salvato in $WIRESHARK_OUTPUT_FILE"    # Avvia Wireshark per analizzare il file di cattura
    echo "Avvio Wireshark..."
    wireshark $WIRESHARK_OUTPUT_FILE &

# Terminare il server iperf
kill "$IPERF_SERVER_PID"
echo "Server iperf terminato."




