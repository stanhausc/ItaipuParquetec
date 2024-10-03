import sys
from . import modbus_functions as mf
from . import auxiliar_modbus_functions as amf
from .modbus_functions import client
from time import sleep
import time
import threading
import csv

#==============================Macros and Definitions============================#
NUMBER_OF_SENSORS = 1
start_value = 0x0000
end_value = 0xFFC0
step_value = 0x007C
INTERVAL_READ_SENSORS = 10

# Estados da máquina de estados
STATE_MEASURE = "INIT"
STATE_ERROR = "ERROR"
STATE_SUCCESS = "SUCCESS"
STATE_FINISHED = "FINISHED"

# Variáveis globais para armazenar o estado atual e o estado de erro
current_state = None
error_flag = 0

#========================= Funções Auxiliares ==========================#
def task_wise_config_init():
    """Inicializa a máquina de estados em uma condição específica."""
    global current_state
    current_state = STATE_MEASURE
    print(f"[DEBUG] Estado inicial definido para: {current_state}")

def append_lists(list1, list2):
    """Adiciona elementos da list1 para a list2 sem criar uma lista de listas."""
    for element in list1:
        list2.append(element)

def decode_integer(data_bin):
    """Decodifica uma sequência de bytes em inteiros de 32 bits."""
    integer = []
    for index in range(0, len(data_bin), 4):
        integer_bin = data_bin[index:index+4]
        byte_array = [integer_bin[1], integer_bin[0]]
        byte_array = [bytes([x]) for x in byte_array]
        data = b''.join(byte_array)
        integer_value = struct.unpack('h', data)[0]
        integer.append(integer_value)
    return integer

# Função para leitura dos registradores
def read_hold_registers(start_address, number_of_registers, address):
    print(f"[DEBUG] Tentando ler registradores: start_address={start_address}, quantity={number_of_registers}, address={address}")
    resolution = 0.001
    response = mf.read_register_function_three(start_address, number_of_registers, address)

    if response is not None:
        print(f"[DEBUG] Leitura bem-sucedida: {response}")
        response *= resolution
        response = round(response, 2)
    else:
        print("[ERROR] Falha na leitura dos registradores.")
    return response

# Função para salvar dados em um CSV
def save_data_to_csv(sensor_data):
    """Função para armazenar dados do sensor em colunas no CSV."""
    if not sensor_data or all(len(sensor) == 0 for sensor in sensor_data):
        print("[ERROR] Dados do sensor estão vazios. Nada a salvar.")
        return

    print(f"[DEBUG] Salvando dados no arquivo CSV...")
    max_len = max(len(sensor) for sensor in sensor_data)
    for sensor in sensor_data:
        while len(sensor) < max_len:
            sensor.append('')
    with open('sensor_data.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        rows = zip(*sensor_data)
        writer.writerows(rows)
    print(f"[DEBUG] Dados salvos com sucesso no arquivo sensor_data.csv")

# Função principal para ler dados em intervalos
def read_sensors_in_interval(interval):
    """Thread para ler os sensores em um intervalo específico."""
    global current_state, error_flag
    print(f"[DEBUG] Iniciando a leitura dos sensores a cada {interval} segundos.")
    task_wise_config_init()

    while True:
        print(f"[DEBUG] Estado atual: {current_state}")
        if current_state == STATE_MEASURE:
            print("[DEBUG] Iniciando a leitura dos sensores.")
            sensor_raw_data = []
            data_velocity_rms = []
            data_acceleration_rms = []
            data_acceleration_peak = []
            data_temperature = []

            for i in range(NUMBER_OF_SENSORS):  # Ler os dados de cada sensor
                slave_addres = i + 1
                print(f"[DEBUG] Lendo dados do sensor {slave_addres}...")

                # Leitura dos registradores Modbus
                velocity_rms = read_hold_registers(0x00, 110, slave_addres)
                print(f"[DEBUG] Velocidade RMS do sensor {slave_addres}: {velocity_rms}")
                if velocity_rms is not None:
                    data_velocity_rms.append(velocity_rms)
                else:
                    error_flag = 1

            print("[DEBUG] Leitura dos sensores concluída, salvando dados.")
            save_data_to_csv(sensor_raw_data)

            if error_flag == 0:
                print("[DEBUG] Mudando estado para FINALIZADO.")
                current_state = STATE_FINISHED
            elif error_flag == 1:
                print("[ERROR] Erro ao ler o sensor.")
                current_state = STATE_ERROR
            time.sleep(interval)

        elif current_state == STATE_ERROR:
            print(f"[DEBUG] Estado de erro. Tentando reiniciar.")
            current_state = STATE_FINISHED
            time.sleep(interval)

        elif current_state == STATE_FINISHED:
            print("[DEBUG] Estado finalizado. Reiniciando para nova leitura.")
            current_state = STATE_MEASURE  # Reinicia para a próxima rodada

#========================= Execução Principal ==========================#

# Debug inicial e definição de parâmetros
print(f"[DEBUG] Script read_sensor_tasks.py iniciado com os parâmetros: {sys.argv}")
print(f"[DEBUG] Porta COM: {sys.argv[1]}, Sensor ID: {sys.argv[2]}")

# Definir porta e ID do cliente
client.port = sys.argv[1]
print(f"[DEBUG] Configurando porta COM para: {client.port}")

# Testar a conexão com o cliente Modbus
if not client.connect():
    print("[ERROR] Não foi possível conectar ao dispositivo Modbus. Verifique a porta COM e os parâmetros de comunicação.")
else:
    print("[INFO] Conexão estabelecida com sucesso.")

# Inicializar a thread de leitura
print("[DEBUG] Iniciando a thread de leitura de sensores...")
sensor_thread = threading.Thread(target=read_sensors_in_interval, args=(INTERVAL_READ_SENSORS,))
sensor_thread.start()
