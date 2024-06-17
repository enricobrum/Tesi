import serial
import time
import configparser

def send_at_command(serial_port, command, timeout=1):
    """
    Invia un comando AT e riceve la risposta.

    Args:
        serial_port (serial.Serial): Oggetto seriale su cui inviare il comando.
        command (str): Comando AT da inviare.
        timeout (int): Timeout in secondi per attendere la risposta.

    Returns:
        str: Risposta ricevuta dal dispositivo.
    """
    serial_port.write((command + '\r\n').encode())
    time.sleep(timeout)
    response = serial_port.read_all().decode()
    return response

def main():
    # Leggi il file di configurazione
    config = configparser.ConfigParser()
    config.read('config.ini')

    serial_config = config['serial']
    port = serial_config.get('port')
    baudrate = serial_config.getint('baudrate')
    timeout = serial_config.getint('timeout')

    # Configura la porta seriale
    serial_port = serial.Serial(
        port=port,
        baudrate=baudrate,
        timeout=timeout
    )

    if serial_port.isOpen():
        print(f"Porta seriale {serial_port.port} aperta con successo.")
    else:
        print(f"Errore nell'aprire la porta seriale {serial_port.port}.")
        return

    try:
        # Lista di comandi AT da inviare
        at_commands = [
            'AT',
            'AT+CSQ',   # Controlla la qualità del segnale
            'AT+CREG?', # Controlla la registrazione della rete
            'AT+CGMI',  # Controlla il produttore del modulo
            'AT+CGMM',  # Controlla il modello del modulo
        ]

        for command in at_commands:
            print(f"Inviando comando: {command}")
            response = send_at_command(serial_port, command, timeout)
            print(f"Risposta:\n{response}")
            print('-' * 40)

    except Exception as e:
        print(f"Errore durante la comunicazione: {e}")
    finally:
        # Chiudi la porta seriale
        serial_port.close()
        print(f"Porta seriale {serial_port.port} chiusa.")

if __name__ == '__main__':
    main()
