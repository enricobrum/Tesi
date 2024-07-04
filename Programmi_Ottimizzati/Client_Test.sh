#!/bin/bash
chmod +x Wireshark.sh
chmod +x Lettura_File_Config.sh
. Iperf.sh
. Wireshark.sh
source Lettura_File_Config.sh
# Definisci i valori dimensione payload
dim_payload=("8" "16" "32" "64" "128" "256" "512" "1024" "1500")
dim_bw=("80M" "800M" "8G" "72G")
ip_server=$(ini_get_value server ip)
port_server=$(ini_get_value server port)
IPERF_CLIENT_DURATION=$(ini_get_value iperf client_duration)
IPERF_CLIENT_PORT=$(ini_get_value iperf client_port)
IPERF_SERVER_IP=$(ini_get_value iperf ip_server)
IPERF_SERVER_PORT=$(ini_get_value iperf server_port)
for dim in "${dim_bw[@]}" #loop che varia il traffico generato dal client iperf 
  do
    #chiamata a funzione di avvio del client con i parametri passati
    start_iperf_client $IPERF_SERVER_IP $IPERF_CLIENT_PORT $IPERF_CLIENT_DURATION $dim  #salvataggio del pid del processo client iperf in modo da poter sapere quando è terminato
    pid=$!
    #echo "Client iperf avvianto al: $IPERF_SERVER_IP:$IPERF_SERVER_PORT per $IPERF_CLIENT_DURATION s con $dim di bitrate."
    for param1 in "${dim_payload[@]}" #loop che varia la dimensione dei payload dei messaggi scambiati tra client e server
      do
        python3 Client.py --server_host "$ip_server" --server_port "$port_server" --payload_size "$param1" --type_test "$dim" #programma python che avvia il client di test
        wait $!
      done
    wait $pid #aspetta che iperf finisca
  done


