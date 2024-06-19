#!/bin/bash
chmod +x Lettura_File_Config.sh
source ./Lettura_File_Config.sh
WIRESHARK_INTERFACCIA=$(ini_get_value wireshark interfaccia)
WIRESHARK_DURATA=$(ini_get_value wireshark durata)
WIRESHARK_OUTPUT_FILE=$(ini_get_value wireshark output_file)
echo "Avvio cattura dei pacchetti sull'interfaccia $WIRESHARK_INTERFACCIA per $WIRESHARK_DURATA. I dati vengono salvati in $WIRESHARK_OUTPUT_FILE"