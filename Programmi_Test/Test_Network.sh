#!/bin/bash
chmod +x Lettura_File_Config.sh
chmod +x Iperf.sh
chmod +x Wireshark.sh
. Iperf.sh
. Wireshark.sh
source Lettura_File_Config.sh
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
start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT 
PID=$!
sleep 3
start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $IPERF_CLIENT_DURATION
#_____________________________________________________________________________

#_____________________________________________________________________________
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




