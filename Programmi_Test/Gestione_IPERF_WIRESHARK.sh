#!/bin/bash
#Funzione per leggere da file di configurazione
function ini_printdb {
    for i in "${!inidb[@]}"
    do
     split the associative key in to section and key
       echo -n "section  : $(echo $i | cut -f1 -d ' ');"
       echo -n "key  : $(echo $i | cut -f2 -d ' ');"
       echo  "value: ${inidb[$i]}"
    done
}
function ini_get_value {
    section=$1
    key=$2
    echo "${inidb[$section $key]}"
}
ini_loadfile test.ini
ini_printdb



