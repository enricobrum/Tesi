#!/bin/bash

# Nome del file di output per la cattura dei pacchetti
OUTPUT_FILE="cattura_pacchetti.pcapng"

# Interfaccia di rete da usare (modifica in base alla tua configurazione)
INTERFACE="eth0"

# Filtri di cattura (modifica in base ai tuoi requisiti)
# Ad esempio, cattura solo pacchetti tra 192.168.1.1 e 192.168.1.2
SOURCE_IP="192.168.1.1"
DEST_IP="192.168.1.2"
FILTER="host $SOURCE_IP and host $DEST_IP"

# Durata della cattura in secondi (modifica se necessario)
DURATION=60

# Funzione per verificare se un comando è installato
command_exists() {
    command -v "$1" &> /dev/null
}

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

# Stampa l'elenco delle interfacce disponibili
echo "Interfacce di rete disponibili:"
tshark -D

# Chiede all'utente di confermare l'interfaccia di rete da usare
read -p "Inserisci il numero dell'interfaccia di rete da usare (default: $INTERFACE): " user_input_interface
if [ ! -z "$user_input_interface" ]; then
    INTERFACE=$user_input_interface
fi

# Conferma i dettagli della cattura
echo "Dettagli della cattura:"
echo "  Interfaccia di rete: $INTERFACE"
echo "  Indirizzo IP sorgente: $SOURCE_IP"
echo "  Indirizzo IP destinazione: $DEST_IP"
echo "  Durata: $DURATION secondi"
echo "  File di output: $OUTPUT_FILE"

# Chiede all'utente di confermare i dettagli della cattura
read -p "Procedere con la cattura dei pacchetti? (s/n): " confirmation
if [ "$confirmation" != "s" ]; then
    echo "Cattura annullata."
    exit 0
fi

# Cattura i pacchetti con tshark
echo "Avvio cattura dei pacchetti sull'interfaccia $INTERFACE per $DURATION secondi..."
tshark -i $INTERFACE -a duration:$DURATION -f "$FILTER" -w $OUTPUT_FILE

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
