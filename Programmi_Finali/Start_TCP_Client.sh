#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
port_server=$(ini_get_value server port)
dim=$(ini_get_value iperf dim)
#____________________________________________
python3 Client.py --server_host "$ip_server" --server_port "$port_server" --type_test "dim" 
wait $!