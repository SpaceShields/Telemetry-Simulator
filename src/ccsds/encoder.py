import struct
from src.ccsds import time, crc, apid
from src.subsystems import cdh, comms, power, propulsion, thermal, adcs, payload


"""
Purpose of this file: This file contains the implementation of the CCSDS encoder.
It provides functions to encode CCSDS packets, including adding APID, CUC time, and CRC.
The encoder ensures that the packets conform to the CCSDS standards for data transfer.
CCSDS 133.0-B (telemetry source packets)
"""

# define the struct format
# >: big-endian
# f: float (4 bytes)
# f: float
# f: float
# B: uint8
# B: uint8
# f: float
# I: uint32
# H: uint16
# B: uint8
# B: uint8
CDH_STRUCT_FORMAT = ">fffBBfIHBB"
POWER_STRUCT_FORMAT = ">ffffffffBB"
COMMS_STRUCT_FORMAT = ">fffffI4B"
THERMAL_STRUCT_FORMAT = ">fBBBBffB"
ADCS_STRUCT_FORMAT = ">ffffffffff4B"
PROPULSION_STRUCT_FORMAT = ">ffff4BffBB"

def encode_ccsds_cdh_payload(data: dict) -> bytes:
    """
    Encodes CDH telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        processor_temp      -> float
        processor_freq      -> float
        processor_util      -> float
        ram_usage           -> uint8
        disk_usage          -> uint8
        cooling_fan_speed   -> float
        uptime              -> uint32
        watchdog_counter    -> uint16
        software_version    -> uint8
        event_flags         -> uint8 bitfield
    """

    # validate/normalize inputs
    processor_temp = float(data['processor_temp'])
    processor_freq = float(data['processor_freq'])
    processor_util = float(data['processor_util'])
    ram_usage = int(data['ram_usage'])
    disk_usage = int(data['disk_usage'])
    cooling_fan_speed = float(data['cooling_fan_speed'])
    uptime = int(data['uptime'])
    watchdog_counter = int(data['watchdog_counter'])
    software_version = int(data['software_version'])
    event_flags = int(data['event_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        CDH_STRUCT_FORMAT,
        processor_temp,
        processor_freq,
        processor_util,
        ram_usage,
        disk_usage,
        cooling_fan_speed,
        uptime,
        watchdog_counter,
        software_version,
        event_flags
    )
    
    return payload

def encode_ccsds_power_payload(data: dict) -> bytes:
    """
    Encodes Power telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        bus_voltage         -> float
        bus_current         -> float
        battery_voltage     -> float
        battery_current     -> float
        battery_temp        -> float
        state_of_charge     -> float
        solar_array_current -> float
        solar_array_voltage -> float
        eps_mode            -> uint8
        fault_flags         -> uint8
    """
    
    # validate/normalize inputs
    bus_voltage = float(data['bus_voltage'])
    bus_current = float(data['bus_current'])
    battery_voltage = float(data['battery_voltage'])
    battery_current = float(data['battery_current'])
    battery_temp = float(data['battery_temp'])
    state_of_charge = float(data['state_of_charge'])
    solar_array_current = float(data['solar_array_current'])
    solar_array_voltage = float(data['solar_array_voltage'])
    eps_mode = int(data['eps_mode'])  # 0–5
    fault_flags = int(data['fault_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        POWER_STRUCT_FORMAT,
        bus_voltage,
        bus_current,
        battery_voltage,
        battery_current,
        battery_temp,
        state_of_charge,
        solar_array_current,
        solar_array_voltage,
        eps_mode,
        fault_flags
    )
    
    return payload

def encode_ccsds_thermal_payload(data: dict) -> bytes:
    """
    Encodes Thermal telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        average_temp        -> float
        heater_status       -> uint8
        radiator_status     -> uint8
        heat_pipe_status    -> uint8
        thermal_mode        -> uint8
        hot_spot_temp       -> float
        cold_spot_temp      -> float
        thermal_fault_flags -> uint8
    """
    
    # validate/normalize inputs
    average_temp = float(data['average_temp'])
    heater_status = int(data['heater_status'])  # 0 or 1
    radiator_status = int(data['radiator_status'])  # 0 or 1
    heat_pipe_status = int(data['heat_pipe_status'])  # 0 or 1
    thermal_mode = int(data['thermal_mode'])  # 0–4
    hot_spot_temp = float(data['hot_spot_temp'])
    cold_spot_temp = float(data['cold_spot_temp'])
    thermal_fault_flags = int(data['thermal_fault_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        THERMAL_STRUCT_FORMAT,
        average_temp,
        heater_status,
        radiator_status,
        heat_pipe_status,
        thermal_mode,
        hot_spot_temp,
        cold_spot_temp,
        thermal_fault_flags
    )
    
    return payload

def encode_ccsds_comms_payload(data: dict) -> bytes:
    """
    Encodes Communications telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        tx_frequency        -> float
        rx_frequency        -> float
        tx_power            -> float
        rx_signal_strength  -> float
        bit_error_rate      -> float
        frame_sync_errors   -> uint32
        carrier_lock        -> uint8
        modulation_mode     -> uint8
        comms_mode          -> uint8
        comms_fault_flags   -> uint8
    """
    
    # validate/normalize inputs
    tx_frequency = float(data['tx_frequency'])
    rx_frequency = float(data['rx_frequency'])
    tx_power = float(data['tx_power'])
    rx_signal_strength = float(data['rx_signal_strength'])
    bit_error_rate = float(data['bit_error_rate'])
    frame_sync_errors = int(data['frame_sync_errors'])
    carrier_lock = int(data['carrier_lock'])  # 0 or 1
    modulation_mode = int(data['modulation_mode'])  # 0–3
    comms_mode = int(data['comms_mode'])  # 0–4
    comms_fault_flags = int(data['comms_fault_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        COMMS_STRUCT_FORMAT,
        tx_frequency,
        rx_frequency,
        tx_power,
        rx_signal_strength,
        bit_error_rate,
        frame_sync_errors,
        carrier_lock,
        modulation_mode,
        comms_mode,
        comms_fault_flags
    )
    
    return payload

def encode_ccsds_adcs_payload(data: dict) -> bytes:
    """
    Encodes ADCS telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        quat_w             -> float
        quat_x             -> float
        quat_y             -> float
        quat_z             -> float
        ang_velocity_x     -> float
        ang_velocity_y     -> float
        ang_velocity_z     -> float
        mag_field_x        -> float
        mag_field_y        -> float
        mag_field_z        -> float
        sun_sensor_status  -> uint8
        gyro_status        -> uint8
        adcs_mode          -> uint8
        adcs_fault_flags   -> uint8
    """
    
    # validate/normalize inputs
    quat_w = float(data['quat_w'])
    quat_x = float(data['quat_x'])
    quat_y = float(data['quat_y'])
    quat_z = float(data['quat_z'])
    ang_velocity_x = float(data['ang_velocity_x'])
    ang_velocity_y = float(data['ang_velocity_y'])
    ang_velocity_z = float(data['ang_velocity_z'])
    mag_field_x = float(data['mag_field_x'])
    mag_field_y = float(data['mag_field_y'])
    mag_field_z = float(data['mag_field_z'])
    sun_sensor_status = int(data['sun_sensor_status'])  # 0 or 1
    gyro_status = int(data['gyro_status'])  # 0 or 1
    adcs_mode = int(data['adcs_mode'])  # 0–4
    adcs_fault_flags = int(data['adcs_fault_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        ADCS_STRUCT_FORMAT,
        quat_w,
        quat_x,
        quat_y,
        quat_z,
        ang_velocity_x,
        ang_velocity_y,
        ang_velocity_z,
        mag_field_x,
        mag_field_y,
        mag_field_z,
        sun_sensor_status,
        gyro_status,
        adcs_mode,
        adcs_fault_flags
    )
    
    return payload

def encode_ccsds_propulsion_payload(data: dict) -> bytes:
    """
    Encodes Propulsion telemetry data into a CCSDS-compliant payload.
    
    The struct format is:
        fuel_level          -> float
        oxidizer_level      -> float
        tank_pressure       -> float
        feedline_temp       -> float
        valve_status        -> uint8
        thruster_firing     -> uint8
        thruster_mode       -> uint8
        propulsion_fault_flags -> uint8
        rcs_tank_level      -> float
        rcs_tank_pressure   -> float
        rcs_thruster_status -> uint8
        rcs_fault_flags     -> uint8
    """
    
    # validate/normalize inputs
    fuel_level = float(data['fuel_level'])
    oxidizer_level = float(data['oxidizer_level'])
    tank_pressure = float(data['tank_pressure'])
    feedline_temp = float(data['feedline_temp'])
    valve_status = int(data['valve_status'])  # 0 or 1
    thruster_firing = int(data['thruster_firing'])  # 0 or 1
    thruster_mode = int(data['thruster_mode'])  # 0–2
    propulsion_fault_flags = int(data['propulsion_fault_flags'])  # bitfield, 0–255
    rcs_tank_level = float(data['rcs_tank_level'])
    rcs_tank_pressure = float(data['rcs_tank_pressure'])
    rcs_thruster_status = int(data['rcs_thruster_status'])  # 0 or 1
    rcs_fault_flags = int(data['rcs_fault_flags'])  # bitfield, 0–255
    
    # pack it all in one shot
    payload = struct.pack(
        PROPULSION_STRUCT_FORMAT,
        fuel_level,
        oxidizer_level,
        tank_pressure,
        feedline_temp,
        valve_status,
        thruster_firing,
        thruster_mode,
        propulsion_fault_flags,
        rcs_tank_level,
        rcs_tank_pressure,
        rcs_thruster_status,
        rcs_fault_flags
    )
    
    return payload

# Placeholders
def encode_ccsds_primary_header() -> bytes:
    """
    Fields:
        version (3 bits)

        type (1 bit, telemetry = 0)

        secondary header flag (1 bit)

        APID (11 bits)

        sequence flags (2 bits)

        sequence count (14 bits)

        data length (TBD, payload+secondary header minus 1)
    """
    pass

def encode_ccsds_secondary_header() -> bytes:
    """
    use encode_cuc_time() from time.py

    4 bytes

    integrate directly without hardcoding
    """
    pass

def crc_generator() -> bytes:
    """
    reuse append_crc() from crc.py

    append to the entire packet
    """
    pass

def encode_ccsds_packet(data: dict, apid: int, seq_count: int) -> bytes:
    """
    build payload

    build secondary header

    build primary header

    concatenate

    append CRC

    return the finished bytes
    """
    pass