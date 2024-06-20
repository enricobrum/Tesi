#!/bin/bash
#Funzione per l'avvio di un server IPERF passando IP, PORT e file di destinazione dell'output
start_iperf_server(){
    local ip=$1
    local port=$2
    echo "Avvio del server iperf su $ip : $port ..."
    iperf -s -B $ip -p $port 
    echo $! # Restituisce il PID del processo avviato
}
export -f start_iperf_server
#Funzione per l'avvio di un client IPERF passando IP del server, PORT e durata in secondi della comunicazione
start_iperf_client() {
    local ip=$1
    local port=$2
    local duration=$3
    echo "Avvio del client iperf verso $ip:$port per $duration secondi..."
    iperf3 -c $ip -p $port -t $duration 
    echo $!
}
export -f start_iperf_client


