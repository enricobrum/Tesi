#!/bin/bash
./Lettura_File_Config.sh
source ./Lettura_File_Config.sh
valore=$(ini_get_value server1 port)
echo "value: $valore"