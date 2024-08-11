#!/bin/bash
chmod +x Lettura_File_Config.sh
. Iperf.sh
source Lettura_File_Config.sh
# iperf riesce a raggiungere e' un bitrate di 20Mbit/s
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port)
IPERF_CLIENT_DURATA=$(ini_get_value iperf durata)
IPERF_SERVER_IP=$(ini_get_value iperf ip_server)
IPERF_SERVER_PORT=$(ini_get_value iperf server_port)
dim=$(ini_get_value iperf dim)
start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $dim $IPERF_CLIENT_DURATA 
wait $!
