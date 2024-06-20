#!/bin/bash
source Iperf.sh
source Wireshark.sh
source Lettura_File_Config
#___________________________________________________________
#Costanti ottenute tramite il file di configuraazione
IPERF_SERVER_IP=$(ini_get_value iperf ip_server)
IPERF_SERVER_PORT=$(ini_get_value iperf server_port)
IPERF_SERVER_OUTPUT_FILE=$(ini_get_value iperf output_file)
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration)
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port)
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia)
WIRESHARK_DURATA=$(ini_get_value wireshark durata)
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file)
#____________________________________________________________
start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT &
SERVER_PID=$!
sleep 5
avvio_tshark $WIRESHARK_INTERFACCIA $WIRESHARK_DURATA $WIRESHARK_OUTPUT_FILE &
TSHARK_PID=$!
start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $IPERF_CLIENT_DURATION
wait $TSHARK_PID
if [ $? -eq 0 ]; then
    echo "Cattura completata. File salvato in $OUTPUT_FILE"
    
    # Avvia Wireshark per analizzare il file di cattura
    echo "Avvio Wireshark..."
    wireshark $WIRESHARK_OUTPUT_FILE &
else
    echo "Errore nella cattura dei pacchetti."
    exit 1
fi
# Terminare il server iperf
kill $SERVER_PID
echo "Server iperf terminato."




