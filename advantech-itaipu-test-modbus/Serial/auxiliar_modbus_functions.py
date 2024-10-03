"""
Modbus Read_Write Coil implementation.
Created on: 02/10/2024
Authored by: Anderson de Camargo
"""

def store_read_data(data_velocity_rms, data_acceleration_rms, data_acceleration_peak, data_temperature, acceleration_raw_data):
    """Here the user can access the variables reads from the sensor and store in the data bank.
    Args:
        data_velocity_rms: velocity rms converted read from sensor
        data_acceleration_rms: acceleration rms converted read from sensor
        data_acceleration_peak: acceleration peak converted read from sensor
        data_temperature: temperatura data converted from sensor
        acceleration_raw_data: raw acceleration data collected from sensor
    """
    velocity_rms = data_velocity_rms
    acceleration_rms = data_acceleration_rms
    acceleration_peak = data_acceleration_peak
    temperature = data_temperature
    raw_data_acceleration = acceleration_raw_data

    return