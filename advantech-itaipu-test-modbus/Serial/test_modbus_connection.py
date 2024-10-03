import modbus_functions as mf

# Definir a porta COM e o baudrate manualmente
mf.client.port = "COM3"  # Substitua pela sua porta COM correta
mf.client.baudrate = 115200  # Certifique-se de que esse valor corresponda ao seu dispositivo
mf.client.timeout = 3  # Timeout para leitura

# Testar a conexão
print(f"Conectando à porta {mf.client.port}...")
if not mf.client.connect():
    print("[ERROR] Não foi possível conectar ao dispositivo Modbus. Verifique a porta e os parâmetros de comunicação.")
else:
    print("[INFO] Conexão estabelecida com sucesso.")

    # Teste de leitura de um registrador para verificar a comunicação (Use slave em vez de unit)
    try:
        response = mf.client.read_holding_registers(0x00, 1, slave=1)  # Ajuste o 'slave' conforme necessário
        if response.isError():
            print(f"[ERROR] Falha ao ler o registrador: {response}")
        else:
            print(f"[INFO] Leitura bem-sucedida: {response.registers}")
    except Exception as e:
        print(f"[ERROR] Exceção ao tentar ler o registrador: {e}")

# Fechar a conexão após o teste
mf.client.close()
