import tkinter as tk
import customtkinter as ctk
import threading
import subprocess
import os
from Serial import modbus_functions as mf

# Definir o caminho para o script `read_sensor_tasks.py`
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "../Serial/read_sensor_tasks.py")

# Variáveis de log e processo
sensor_process = None
process_running = False
sensor_log = []  # Variável global para armazenar as mensagens do terminal da aba de leitura

# Função para criar a aba de leitura de sensores
def create_sensor_tab(parent_frame):
    global sensor_process, process_running, sensor_log

    # Obtém as variáveis de configuração do módulo Modbus
    com_port = mf.client.port
    sensor_id = mf.current_sensor_id

    sensor_frame = ctk.CTkFrame(parent_frame)
    sensor_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título da Aba de Sensores
    sensor_label = ctk.CTkLabel(sensor_frame, text="Leitura de Sensores", font=ctk.CTkFont(size=20, weight="bold"))
    sensor_label.pack(pady=15)

    # Área de exibição do terminal
    terminal_output = tk.Text(sensor_frame, height=15, width=100)
    terminal_output.pack(pady=15)

    # Atualiza o terminal com o histórico de log
    update_terminal(terminal_output, sensor_log)

    # Função para iniciar a leitura do sensor
    def start_sensor_reading():  # A função deve ter o bloco de código indentado corretamente
        global sensor_process, process_running, sensor_log
        if sensor_process is None:
            log_message = f"[INFO] Iniciando leitura dos sensores na Porta COM = {com_port}, ID = {sensor_id}...\n"
            sensor_log.append(log_message)
            update_terminal(terminal_output, sensor_log)

            # Executa a leitura em um thread separado
            threading.Thread(target=run_sensor_script, args=(terminal_output, com_port, sensor_id)).start()
        else:
            sensor_log.append("[ERROR] Leitura já em execução.\n")
            update_terminal(terminal_output, sensor_log)

    # Função para rodar o script de leitura
    def run_sensor_script(terminal_widget, com_port, sensor_id):
        global sensor_process, process_running, sensor_log
        process_running = True
        try:
            command = ["python", SCRIPT_PATH, com_port, str(sensor_id)]
            print(f"[DEBUG] Executando: {' '.join(command)}")  # Adiciona logs para verificar o comando
            sensor_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
            )

            while process_running:
                output = sensor_process.stdout.readline()
                if output:
                    sensor_log.append(output)
                    terminal_widget.insert(tk.END, output)
                    terminal_widget.see(tk.END)
                else:
                    break
        except Exception as e:
            terminal_widget.insert(tk.END, f"[ERROR] Falha ao executar: {str(e)}\n")


    # Função para parar a leitura do sensor
    def stop_sensor_reading():
        global sensor_process, process_running, sensor_log
        if sensor_process:
            process_running = False
            sensor_process.terminate()
            sensor_process = None
            log_message = f"[INFO] Leitura interrompida pelo usuário para a Porta COM = {com_port}, ID = {sensor_id}.\n"
            sensor_log.append(log_message)
            update_terminal(terminal_output, sensor_log)

    # Botões de Controle de Leitura
    start_button = ctk.CTkButton(sensor_frame, text="Iniciar Leitura", command=start_sensor_reading, width=150)
    start_button.pack(pady=10)

    stop_button = ctk.CTkButton(sensor_frame, text="Parar Leitura", command=stop_sensor_reading, width=150)
    stop_button.pack(pady=10)

# Função para atualizar o terminal com as mensagens armazenadas
def update_terminal(terminal_widget, messages):
    terminal_widget.delete("1.0", tk.END)  # Limpa o terminal
    for message in messages:
        terminal_widget.insert(tk.END, message)  # Insere as mensagens do log
    terminal_widget.see(tk.END)  # Mantém a rolagem automática
