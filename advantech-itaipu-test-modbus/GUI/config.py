# GUI/config.py
import tkinter as tk
import customtkinter as ctk
import threading
import os
from Serial import com_scan

# Variáveis globais para armazenar configurações dinâmicas
current_com_port = "COM4"
current_sensor_id = "1"
sensor_process = None
process_running = False  # Flag para controle de execução

# Caminho correto para o script de leitura
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "../Serial/read_sensor_tasks.py")

# Função para criar a aba de Configuração
def create_config_frame(config_frame, notebook):
    global current_com_port, current_sensor_id

    # Título da Aba de Configurações
    config_label = ctk.CTkLabel(config_frame, text="Configurações de Comunicação e Leitura", font=ctk.CTkFont(size=20, weight="bold"))
    config_label.pack(pady=15)

    # Linha para exibir campos e botões lado a lado
    com_id_frame = ctk.CTkFrame(config_frame)
    com_id_frame.pack(pady=10)

    # Seção de Configuração de Porta COM
    com_section_label = ctk.CTkLabel(com_id_frame, text="Porta COM:", font=ctk.CTkFont(size=16, weight="bold"))
    com_section_label.grid(row=0, column=0, padx=5)

    port_combobox = ctk.CTkComboBox(com_id_frame, width=150, state="readonly")
    port_combobox.grid(row=0, column=1, padx=5)
    port_combobox.set(current_com_port)

    # Botão para escanear portas COM
    def scan_com_ports():
        ports = com_scan.scan_ports()
        port_combobox.configure(values=ports)
        if ports:
            port_combobox.set(ports[0])

    scan_button = ctk.CTkButton(com_id_frame, text="Scan COM Ports", command=scan_com_ports, width=150)
    scan_button.grid(row=0, column=2, padx=5)

    # Campo para ID do Sensor
    id_label = ctk.CTkLabel(com_id_frame, text="ID do Sensor:", font=ctk.CTkFont(size=16, weight="bold"))
    id_label.grid(row=0, column=3, padx=5)
    id_entry = ctk.CTkEntry(com_id_frame, placeholder_text="Ex: 1", width=100)
    id_entry.grid(row=0, column=4, padx=5)
    id_entry.insert(0, current_sensor_id)

    # Botão para Salvar a Configuração
    def save_config():
        global current_com_port, current_sensor_id
        current_com_port = port_combobox.get()
        current_sensor_id = id_entry.get()
        terminal_output.insert(tk.END, f"[INFO] Configurações Salvas: Porta COM = {current_com_port}, ID = {current_sensor_id}\n")

    save_button = ctk.CTkButton(config_frame, text="Salvar Configurações", command=save_config, width=200)
    save_button.pack(pady=15)

    # Seção de Controle de Leitura
    control_section_label = ctk.CTkLabel(config_frame, text="Controle de Leitura do Sensor", font=ctk.CTkFont(size=16, weight="bold"))
    control_section_label.pack(pady=15)

    # Botões de Controle de Leitura lado a lado
    control_frame = ctk.CTkFrame(config_frame)
    control_frame.pack(pady=10)

    # Botão para Iniciar a Leitura do Sensor
    start_button = ctk.CTkButton(control_frame, text="Iniciar Leitura", width=150)
    start_button.grid(row=0, column=0, padx=10)

    # Botão para Parar a Leitura
    stop_button = ctk.CTkButton(control_frame, text="Parar Leitura", width=150)
    stop_button.grid(row=0, column=1, padx=10)

    # Área para exibir mensagens de terminal
    global terminal_output
    terminal_output = tk.Text(config_frame, height=15, width=100)
    terminal_output.pack(pady=15)
