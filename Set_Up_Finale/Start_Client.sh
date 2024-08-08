#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
port_server=$(ini_get_value server port)
intervals=$(ini_get_value client intervals)
#____________________________________________
python3 Client.py --server_host "$ip_server" --server_port "$port_server" --intervals $intervals
wait $!
