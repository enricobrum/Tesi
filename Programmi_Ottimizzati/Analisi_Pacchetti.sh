#!/bin/bash

# Verifica che siano stati passati i parametri necessari
if [ "$#" -ne 3 ]; then
    echo "Uso: $0 <file.pcapng> <indirizzo IP> <output.csv>"
    exit 1
fi

# Parametri
PCAP_FILE=$1
IP_ADDRESS=$2
OUTPUT_CSV=$3

# Estrazione dei pacchetti relativi all'indirizzo IP specificato
tshark -r "$PCAP_FILE" -Y "ip.src == $IP_ADDRESS || ip.dst == $IP_ADDRESS" -T fields -e frame.number -e frame.time -e ip.src -e ip.dst -e ip.proto -e ip.len -e frame.len -E header=y -E separator=, -E quote=d > "$OUTPUT_CSV"

echo "Estrazione completata. I dati sono stati salvati in $OUTPUT_CSV"
