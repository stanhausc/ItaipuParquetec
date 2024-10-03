#!/usr/bin/env python3
"""
Modbus Read_Write Coil implementation.
Created on: 21/08/2024
Authored by: Anderson de Camargo
"""
import pymodbus.client as modbus_client
from . import auxiliar_modbus_functions as amf

from typing import Optional

from pymodbus import (
    FramerType,
    ModbusException,
)

from pymodbus.pdu.file_message import FileRecord

# Definição do cliente Modbus
client = modbus_client.ModbusSerialClient(
    'COM3',
    framer=FramerType.RTU,
    baudrate=115200,
    bytesize=8,
    parity="N",
    stopbits=1,
)


client.port = 'COM3' # Adicionar manualmente o atributo `port` para permitir acesso externo
current_sensor_id = 1  # ID padrão para inicialização


def read_register_function_three(start_addres, quantity_registers, address) -> Optional[int]:
    """
    Aux function to read modbus holding registers.
    Args:
    Returns:
        None:
    """
    # response = None
    try:
        response = client.read_holding_registers(start_addres, quantity_registers, address)
        response = (response.registers[1] << 8) | response.registers[0]
    except ModbusException:
        response = None

    return response

def write_modbus_coil_addr(coil_addr, on_off, slave_addr):
    """
    Aux function to write modBus coil addresses.

    Args:
        coil_addr (int): The address of the coil.
        on_off (bool): The state of the coil.
        slave_addr (int): The address of the slave.
    Returns:
        int: Nothing at the moment.
    """
    # response = None
    try:
        response = client.write_coil(coil_addr, on_off, slave_addr)
    except ModbusException:
        response = None
    return response

def read_modbus_coil_add(coil_addr, number_of_coils, slave_addr):
    """
    Aux function to read modBus coil status.

    Args:
        coil_addr (int): The address of the coil.
        number_of_coils (int): Quantity of coils to be read.
        slave_addr (int): The address of the slave.
    Returns:
        int: Nothing at the moment.
    """
    # response = None

    try:
        response = client.read_coils(coil_addr, number_of_coils, slave_addr)
    except ModbusException:
        response = None
    return response

def read_file(file_n, record_n, length, slave_addr):
    """
    Aux function to record the file.

    Args:
        file_n (int): Number of the file to query raw data
        record_n (int): Start record number within the file
        length (int):  Record length - maximum amount of data transferred in a single Modbus/RTU request
        slave_addr (int):  Slave address
    Returns:
        int: Nothing at the moment.
    """
    # response = None
    records = FileRecord(
        file_number = file_n,
        record_number = record_n,
        record_length = length
    )

    try:
        response = client.read_file_record([records], slave_addr)
    except ModbusException:
        response = None
    return response



