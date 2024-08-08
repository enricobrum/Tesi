#!/bin/bash
chmod +x Lettura_File_Config.sh
source Lettura_File_Config.sh
#____________________________________________
ip_server=$(ini_get_value server ip)
port_tcp=$(ini_get_value server port_tcp)
port_udp=$(ini_get_value server port_udp)
intervals=$(ini_get_value client intervals)
#____________________________________________
sudo python3 Client_finale.py --server_host "$ip_server" --tcp_port "$port_tcp" --udp_port "$port_udp" --intervals "$intervals"
wait $!
