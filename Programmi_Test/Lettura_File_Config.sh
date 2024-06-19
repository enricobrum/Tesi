#!/bin/bash
#Funzione per leggere da file di configurazione
declare -A inidb
function _ini_get_section {
    if [[ "$1" =~ ^(\[)(.*)(\])$ ]]; 
    then 
        echo ${BASH_REMATCH[2]} ; 
    else 
        echo ""; 
    fi
}
function _ini_get_key_value {
    if [[ "$1" =~ ^([^=]+)=([^=]+)$ ]]; 
    then 
        echo "${BASH_REMATCH[1]}=${BASH_REMATCH[2]}"; 
    else 
        echo ""
    fi
}
function ini_printdb {
    for i in "${!inidb[@]}"
    do
    # split the associative key in to section and key
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
function ini_loadfile {
    local cur_section=""
    local cur_key=""
    local cur_val=""
    IFS=
    while read -r line; do
        new_section=$(_ini_get_section $line)
     #    got a new section
        if [[ -n "$new_section" ]]; then
            cur_section=$new_section
        # not a section, try a key value
        else
            val=$(_ini_get_key_value $line)
            # trim the leading and trailing spaces as well
            cur_key=$(echo $val | cut -f1 -d'=' | sed -e 's/^[[:space:]]*//' | sed -e 's/[[:space:]]*$//') 
            cur_val=$(echo $val | cut -f2 -d'=' | sed -e 's/^[[:space:]]*//' | sed -e 's/[[:space:]]*$//')
        if [[ -n "$cur_key" ]]; then
            # section + key is the associative in bash array, the field seperator is space
            inidb[${cur_section} ${cur_key}]=$cur_val
        fi
    fi
    done <$1
}
ini_loadfile config.ini
ini_printdb
echo "value: ${inidb[!inidb[1]]}"




