#!/bin/bash
chmod +x Lettura_File_Config.sh
source ./Lettura_File_Config.sh
IPERF_SERVER_IP=$(ini_get_value iperf ip)
echo "$IPER_SERVER_IP"
IPERF_SERVER_PORT=$(ini_get_value iperf port)
IPERF_SERVER_OUTPUT_FILE=$(ini_get_value iperf output_file)
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration)
#Funzione per l'avvio di un server IPERF passando IP, PORT e file di destinazione dell'output
start_iperf_server(){
    ip=$1
    port=$2
    output_file=$3
    echo "Avvio del server iperf su $ip : $port ..."
    iperf3 -s -B $ip -p $port > $output_file 2>&1 &
    echo $! # Restituisce il PID del processo avviato
}
#Funzione per l'avvio di un client IPERF passando IP del server, PORT e durata in secondi della comunicazione
start_iperf_client() {
    echo "Avvio del client iperf verso $SERVER_IP:$PORT per $DURATION secondi..."
    iperf3 -c $IPERF_SERVER_IP -p $IPERF_SERVER_PORT -t $IPERF_CLIENT_DURATION
}
IPERF_CLIENT_PID=$(start_iperf_client $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_CLIENT_DURATION)
IPERF_SERVER_PID=$(start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_SERVER_OUTPUT_FILE)
echo $IPERF_SERVER_PID