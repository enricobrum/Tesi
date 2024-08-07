#!/bin/bash
#Funzione per l'avvio di un server IPERF passando IP, 
#PORT e file di destinazione dell'output
start_iperf_server(){
    local ip=$1
    local port=$2
    echo "Avvio del server iperf su $ip : $port ..."
    iperf3 -s -B $ip -p $port &
}
#Funzione per l'avvio di un client IPERF passando
# IP del server, PORT della comunicazione
start_iperf_client() {
    local ip=$1
    local port=$2
    local bitrate=$3
    local durata=$4
    iperf3 -c $ip -p $port -b $bitrate -t $durata &
    return $!
}



