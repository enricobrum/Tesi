#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
# Definisci i valori dimensione payload
dim_payload=("8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" "16384" "32768" "65536")
ip_server=$(ini_get_value server ip)
port_server=$(ini_get_value server port)
python3 Server.py --host "$ip_server" --port "$port_server" &
sleep 5
for param1 in "${dim_payload[@]}"
    do
      python3 Client.py --server_host "$ip_server" --server_port "$port_server" --payload_size "$param1"
done
