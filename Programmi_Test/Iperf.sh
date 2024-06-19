#!/bin/bash
#Funzione per l'avvio di un server IPERF passando IP, PORT e file di destinazione dell'output
start_iperf_server(){
    ip=$1
    port=$2
    output_file=$3
    echo "Avvio del server iperf su $ip : $port ..."
    iperf3 -s -B $ip -p $port > $output_file 2>&1 &
    echo $! # Restituisce il PID del processo avviato
}
#Funzione per l'avvio di un client IPERF passando IP del server, PORT e durata in secondi della comunicazione
start_iperf_client() {
    ip=$1
    port=$2
    duration=$3
    echo "Avvio del client iperf verso $SERVER_IP:$PORT per $DURATION secondi..."
    iperf3 -c $ip -p $port -t $duration
    echo $!
}


