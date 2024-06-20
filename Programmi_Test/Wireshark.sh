#!/bin/bash
avvio_tshark(){
    local interfaccia=$1
    local durata=$2
    local output_file=$3
    echo "Avvio cattura dei pacchetti sull'interfaccia $interfaccia per $durata s. I dati vengono salvati in $output_file ..."
    tshark -i $interfaccia -a duration:$durata -w $output_file 
    echo $!
}
export -f avvio_tshark
