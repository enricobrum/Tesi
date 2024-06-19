#!/bin/bash
function avvio_tshark(){
    interfaccia = $1
    durata = $2
    output_file = $3
    echo "Avvio cattura dei pacchetti sull'interfaccia $WIRESHARK_INTERFACCIA per $WIRESHARK_DURATA s. I dati vengono salvati in $WIRESHARK_OUTPUT_FILE ..."
    tshark -i $interfaccia -a duration:$durata -w $output_file &
    echo $!
}
