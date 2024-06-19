#!/bin/bash
chmod +x Lettura_File_Config.sh
source ./Lettura_File_Config.sh
IPERF_SERVER_IP=$(ini_get_value iperf ip)
echo "$IPER_SERVER_IP"
IPERF_SERVER_PORT=$(ini_get_value iperf port)
IPERF_SERVER_OUTPUT_FILE=$(ini_get_value iperf output_file)
start_iperf_server(){
    ip=$1
    port=$2
    output_file=$3
    echo "Avvio del server iperf su $ip : $port ..."
    iperf3 -s -B $ip -p $port > $output_file 2>&1 &
    echo $! # Restituisce il PID del processo avviato
}
IPERF_SERVER_PID=$(start_iperf_server $IPERF_SERVER_IP $IPERF_SERVER_PORT $IPERF_SERVER_OUTPUT_FILE)
echo $IPERF_SERVER_PID