#!/bin/bash

# Definisci i valori per param1 e param2
param1_values=("8" "16" "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" "16384" "32768" "65536")

# Itera sui valori di param1
for param1 in "${param1_values[@]}"
  do
    # Esegui lo script Python con i parametri correnti
    python3 Server_TCP.py --payload_size "$param1" 
  done
done
