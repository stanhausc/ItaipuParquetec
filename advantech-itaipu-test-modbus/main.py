from GUI.main_window import create_config_frame
from GUI.sensor_tab import create_sensor_tab

import customtkinter as ctk

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("Dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema de cores

# Função para iniciar a interface principal
def main():
    main_window = ctk.CTk()
    main_window.title("Interface Principal de Leitura e Configuração")
    main_window.geometry("1024x768")

    # Frame de Navegação à Esquerda
    navigation_frame = ctk.CTkFrame(main_window, width=200)
    navigation_frame.pack(side="left", fill="y")

    # Frame de Conteúdo à Direita
    content_frame = ctk.CTkFrame(main_window, width=800, height=600)
    content_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

    # Função para alternar entre frames de conteúdo
    def show_frame(frame_func):
        for widget in content_frame.winfo_children():
            widget.destroy()
        frame_func(content_frame)  # Exibe a aba selecionada no frame de conteúdo

    # Botões de Navegação para Alternar Entre as Abas
    config_button = ctk.CTkButton(navigation_frame, text="Configurações", command=lambda: show_frame(create_config_frame))
    config_button.pack(pady=20, padx=20)

    sensor_button = ctk.CTkButton(navigation_frame, text="Leitura de Sensores", command=lambda: show_frame(create_sensor_tab))
    sensor_button.pack(pady=20, padx=20)

    # Iniciar com a aba de configurações
    show_frame(create_config_frame)
    
    main_window.mainloop()

# Executa a interface principal
if __name__ == "__main__":
    main()
