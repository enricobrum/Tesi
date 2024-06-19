#!/bin/bash
chmod +x Lettura_File_Config.sh
chmod +x Iperf.sh
chmod +x Wireshark.sh
source ./Lettura_File_Config.sh
source ./Iperf.sh
source ./Wireshark.sh
#___________________________________________________________
#Costanti ottenute tramite il file di configuraazione
IPERF_SERVER_IP=$(ini_get_value iperf ip)
IPERF_SERVER_PORT=$(ini_get_value iperf port)
IPERF_SERVER_OUTPUT_FILE=$(ini_get_value iperf output_file)
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration)

WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia)
WIRESHARK_DURATA=$(ini_get_value wireshark durata)
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file)
#____________________________________________________________
IPERF_SERVER_PID=$(start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_SERVER_OUTPUT_FILE)
sleep 5
WIRESHARK_PID=$(avvio_tshark $WIRESHARK_INTERFACCIA $WIRESHARK_DURATA $WIRESHARK_OUTPUT_FILE)
start_iperf_client $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_CLIENT_DURATION
wait $WIRESHARK_PID
# Controlla se la cattura è stata completata con successo
if [ $? -eq 0 ]; then
    echo "Cattura completata. File salvato in $WIRESHARK_OUTPUT_FILE"
    
    # Avvia Wireshark per analizzare il file di cattura
    echo "Avvio Wireshark..."
    wireshark $WIRESHARK_OUTPUT_FILE &
else
    echo "Errore nella cattura dei pacchetti."
    exit 1
fi

# Terminare il server iperf
kill $IPERF_SERVER_PID
echo "Server iperf terminato."



