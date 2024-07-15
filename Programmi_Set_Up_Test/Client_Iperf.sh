#!/bin/bash
chmod +x Wireshark.sh
chmod +x Lettura_File_Config.sh
. Iperf.sh
. Wireshark.sh
source Lettura_File_Config.sh
dim_bw=("1M" "8M" "10M" "80M") #il limite di test sulla rete che
# iperf riesce a raggiungere e' un bitrate di 20Mbit/s
ip_server=$(ini_get_value server ip)
port_server=$(ini_get_value server port)
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port)
IPERF_SERVER_IP=$(ini_get_value iperf ip_server)
IPERF_SERVER_PORT=$(ini_get_value iperf server_port)
for dim in "${dim_bw[@]}" #loop che varia il traffico generato dal client iperf 
  do
    #chiamata a funzione di avvio del client con i parametri passati
    start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $dim 
    #programma python che avvia il client di test
        python3 Client.py --server_host "$ip_server" --server_port "$port_server" --type_test "$dim" 
        wait $!
      done
    killall iperf3
  done


