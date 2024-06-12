#!/bin/bash

# Definisci i valori dimensione payload
dim_payload=("8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" "16384" "32768" "65536")

# Itera sui valori di param1
for param1 in "${dim_payload[@]}"
  do
    # Esegui lo script Python con i parametri correnti
    gnome-terminal -- bash -c "python3 Client_TCP.py --payload_size "$dim_payload"; exec bash" 
done
