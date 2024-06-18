#!/bin/bash
#Funzione per leggere da file di configurazione
get_config_value() {
    local section="$1"
    local key="$2"
    local config_file="$3"
    local value
    valure=$(awk '/^\[/ { app=substr($0,2,length-2) } /=/ { print app "." $0 }' file.conf)
    echo "$value"
}


#Leggo i valori dei file di configurazione:
CONFIG_FILE="config.ini"
# Parametri nodo centrale
echo CENTRAL_IP=$(get_config_value "nodo_centrale" "ip" "$CONFIG_FILE")
echo DURATION=$(get_config_value "nodo_centrale" "duration" "$CONFIG_FILE")
echo INTERFACE=$(get_config_value "nodo_centrale" "interface" "$CONFIG_FILE")
echo TSHARK_OUTPUT_FILE=$(get_config_value "nodo_centrale" "tshark_output_file" "$CONFIG_FILE")
# Parametri server
echo SERVER1_IP=$(get_config_value "server1" "ip" "$CONFIG_FILE")
echo SERVER1_PORT=$(get_config_value "server1" "port" "$CONFIG_FILE")
echo SERVER1_IPERF_OUTPUT_FILE=$(get_config_value "server1" "iperf_output_file" "$CONFIG_FILE")
echo SERVER2_IP=$(get_config_value "server2" "ip" "$CONFIG_FILE")
echo SERVER2_PORT=$(get_config_value "server2" "port" "$CONFIG_FILE")
echo SERVER2_IPERF_OUTPUT_FILE=$(get_config_value "server2" "iperf_output_file" "$CONFIG_FILE")

