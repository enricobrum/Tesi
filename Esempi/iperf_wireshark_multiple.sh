#!/bin/bash

# Funzione per leggere i valori di configurazione dal file ini
get_config_value() {
    section=$1
    key=$2
    config_file=$3
    value=$(sed -n "/^\[$section\]/,/^\[/{/^[^#].*=/p;}" "$config_file" | grep "^$key=" | cut -d '=' -f2 | tr -d ' ')
    echo $value
}

# Leggi i valori di configurazione dal file config.ini
CONFIG_FILE="config.ini"

# Parametri nodo centrale
CENTRAL_IP=$(get_config_value "nodo_centrale" "ip" "$CONFIG_FILE")
DURATION=$(get_config_value "nodo_centrale" "duration" "$CONFIG_FILE")
INTERFACE=$(get_config_value "nodo_centrale" "interface" "$CONFIG_FILE")
TSHARK_OUTPUT_FILE=$(get_config_value "nodo_centrale" "tshark_output_file" "$CONFIG_FILE")

# Parametri server
SERVER1_IP=$(get_config_value "server1" "ip" "$CONFIG_FILE")
SERVER1_PORT=$(get_config_value "server1" "port" "$CONFIG_FILE")
SERVER1_IPERF_OUTPUT_FILE=$(get_config_value "server1" "iperf_output_file" "$CONFIG_FILE")
SERVER2_IP=$(get_config_value "server2" "ip" "$CONFIG_FILE")
SERVER2_PORT=$(get_config_value "server2" "port" "$CONFIG_FILE")
SERVER2_IPERF_OUTPUT_FILE=$(get_config_value "server2" "iperf_output_file" "$CONFIG_FILE")

# Funzione per verificare se un comando è installato
command_exists() {
    command -v "$1" &> /dev/null
}

# Controlla se iperf3 è installato
if ! command_exists iperf3; then
    echo "Errore: iperf3 non è installato. Installalo prima di eseguire questo script."
    exit 1
fi

# Controlla se tshark è installato
if ! command_exists tshark; then
    echo "Errore: tshark non è installato. Installalo prima di eseguire questo script."
    exit 1
fi

# Controlla se Wireshark è installato
if ! command_exists wireshark; then
    echo "Errore: Wireshark non è installato. Installalo prima di eseguire questo script."
    exit 1
fi

# Funzione per avviare un server iperf
start_iperf_server() {
    local ip=$1
    local port=$2
    local output_file=$3
    echo "Avvio del server iperf su $ip:$port..."
    iperf3 -s -B $ip -p $port > $output_file 2>&1 &
    echo $! # Restituisce il PID del processo avviato
}

# Avvia i server iperf
SERVER1_PID=$(start_iperf_server $SERVER1_IP $SERVER1_PORT $SERVER1_IPERF_OUTPUT_FILE)
SERVER2_PID=$(start_iperf_server $SERVER2_IP $SERVER2_PORT $SERVER2_IPERF_OUTPUT_FILE)

# Attendere un momento per assicurarsi che i server siano avviati
sleep 5

# Cattura i pacchetti con tshark
echo "Avvio cattura dei pacchetti sull'interfaccia $INTERFACE per $DURATION secondi..."
tshark -i $INTERFACE -a duration:$DURATION -w $TSHARK_OUTPUT_FILE &
TSHARK_PID=$!

# Avvia il client iperf verso il nodo centrale
echo "Avvio del client iperf verso il nodo centrale $CENTRAL_IP..."
iperf3 -c $CENTRAL_IP -p $SERVER1_PORT -t $DURATION &
iperf3 -c $CENTRAL_IP -p $SERVER2_PORT -t $DURATION &

# Attendere la fine della cattura
wait $TSHARK_PID

# Controlla se la cattura è stata completata con successo
if [ $? -eq 0 ]; then
    echo "Cattura completata. File salvato in $TSHARK_OUTPUT_FILE"
else
    echo "Errore nella cattura dei pacchetti."
    exit 1
fi

# Terminare i server iperf
kill $SERVER1_PID
kill $SERVER2_PID
echo "Server iperf terminati."
