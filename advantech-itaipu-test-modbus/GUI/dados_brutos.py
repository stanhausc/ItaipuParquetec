# GUI/dados_brutos.py
import tkinter as tk
import customtkinter as ctk

# Função para criar a aba de Dados Brutos
def create_raw_data_frame(raw_data_frame, notebook):
    # Terminal de dados brutos
    global raw_data_output
    raw_data_output = tk.Text(raw_data_frame, height=15, width=100)
    raw_data_output.pack(pady=15)
