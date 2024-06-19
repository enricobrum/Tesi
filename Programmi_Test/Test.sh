#!/bin/bash
chmod +x Lettura_File_Config.sh
source ./Lettura_File_Config.sh
echo "$(ini_get_value server1 ip)"

