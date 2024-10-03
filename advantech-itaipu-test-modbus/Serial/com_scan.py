# Serial/com_scan.py
import serial.tools.list_ports

def scan_ports():
    """
    Escaneia as portas COM disponíveis no sistema.
    Retorna uma lista com as portas encontradas.
    """
    ports = serial.tools.list_ports.comports()
    available_ports = [port.device for port in ports]
    return available_ports

if __name__ == "__main__":
    print(scan_ports())
