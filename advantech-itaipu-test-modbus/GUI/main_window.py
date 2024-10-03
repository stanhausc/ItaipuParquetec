import customtkinter as ctk
import tkinter as tk
from Serial import com_scan  # Importa o script de scan de portas COM
from Serial import modbus_functions as mf  # Importa o módulo modificado

# Função para criar o frame de configuração
def create_config_frame(parent_frame):
    # Obtém as variáveis de configuração atuais diretamente do módulo Modbus
    current_com_port = mf.client.port
    current_sensor_id = mf.current_sensor_id  # Agora esse atributo está disponível

    config_frame = ctk.CTkFrame(parent_frame)
    config_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título da Aba de Configurações
    config_label = ctk.CTkLabel(config_frame, text="Configurações de Comunicação e Leitura", font=ctk.CTkFont(size=20, weight="bold"))
    config_label.pack(pady=15)

    com_id_frame = ctk.CTkFrame(config_frame)
    com_id_frame.pack(pady=10)

    # Botão para escanear portas COM
    scan_button = ctk.CTkButton(com_id_frame, text="Scan COM Ports", command=lambda: scan_com_ports(port_combobox), width=150)
    scan_button.grid(row=0, column=0, padx=5)

    com_section_label = ctk.CTkLabel(com_id_frame, text="Porta COM:", font=ctk.CTkFont(size=16, weight="bold"))
    com_section_label.grid(row=0, column=1, padx=5)

    port_combobox = ctk.CTkComboBox(com_id_frame, width=150, state="readonly")
    port_combobox.grid(row=0, column=2, padx=5)
    port_combobox.set(current_com_port)

    id_label = ctk.CTkLabel(com_id_frame, text="ID do Sensor:", font=ctk.CTkFont(size=16, weight="bold"))
    id_label.grid(row=0, column=3, padx=5)
    id_entry = ctk.CTkEntry(com_id_frame, placeholder_text="Ex: 1", width=100)
    id_entry.grid(row=0, column=4, padx=5)
    id_entry.insert(0, str(current_sensor_id))

    # Função para salvar as configurações e atualizar as variáveis no módulo
    def save_config():
        mf.client.port = port_combobox.get()  # Atualiza a porta COM no módulo Modbus
        mf.current_sensor_id = int(id_entry.get())  # Atualiza o ID do sensor
        log_message = f"[INFO] Configurações Salvas: Porta COM = {mf.client.port}, ID = {mf.current_sensor_id}\n"
        terminal_output.insert(tk.END, log_message)

    save_button = ctk.CTkButton(config_frame, text="Salvar Configurações", command=save_config, width=200)
    save_button.pack(pady=15)

    # Área para exibir mensagens do terminal
    terminal_output = tk.Text(config_frame, height=10, width=80)
    terminal_output.pack(pady=15)

# Função para escanear as portas COM e atualizar o combobox
def scan_com_ports(port_combobox):
    ports = com_scan.scan_ports()
    port_combobox.configure(values=ports)
    if ports:
        port_combobox.set(ports[0])
