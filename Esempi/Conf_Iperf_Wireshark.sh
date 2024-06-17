#!/bin/bash

# Nome del file di output per la cattura dei pacchetti
OUTPUT_FILE="cattura_iperf.pcapng"

# Interfaccia di rete da usare (modifica in base alla tua configurazione)
INTERFACE="eth0"

# Indirizzo IP del server iperf
SERVER_IP="192.168.1.2"

# Porta del server iperf
PORT=5201

# Durata del test iperf in secondi
DURATION=60

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

# Funzione per avviare il server iperf
start_iperf_server() {
    echo "Avvio del server iperf su $SERVER_IP:$PORT..."
    iperf3 -s -p $PORT &
    SERVER_PID=$!
    echo "Server iperf avviato con PID $SERVER_PID"
}

# Funzione per avviare il client iperf
start_iperf_client() {
    echo "Avvio del client iperf verso $SERVER_IP:$PORT per $DURATION secondi..."
    iperf3 -c $SERVER_IP -p $PORT -t $DURATION
}

# Avvio del server iperf
start_iperf_server

# Attendere un momento per assicurarsi che il server sia avviato
sleep 5

# Cattura i pacchetti con tshark
echo "Avvio cattura dei pacchetti sull'interfaccia $INTERFACE per $DURATION secondi..."
tshark -i $INTERFACE -a duration:$DURATION -w $OUTPUT_FILE &
TSHARK_PID=$!

# Avvio del client iperf
start_iperf_client

# Attendere la fine della cattura
wait $TSHARK_PID

# Controlla se la cattura è stata completata con successo
if [ $? -eq 0 ]; then
    echo "Cattura completata. File salvato in $OUTPUT_FILE"
    
    # Avvia Wireshark per analizzare il file di cattura
    echo "Avvio Wireshark..."
    wireshark $OUTPUT_FILE &
else
    echo "Errore nella cattura dei pacchetti."
    exit 1
fi

# Terminare il server iperf
kill $SERVER_PID
echo "Server iperf terminato."
