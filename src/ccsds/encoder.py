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