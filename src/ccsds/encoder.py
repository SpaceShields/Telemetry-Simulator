import struct
from src.ccsds import time, crc, apid
from src.subsystems import cdh, comms, power, propulsion, thermal, adcs, payload
import sys
sys.path.append("src")

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
    
payload_temp = encode_ccsds_cdh_payload(cdh.get_cdh_telemetry())
print(payload_temp)
def decode_ccsds_cdh_payload(payload: bytes) -> dict:
    fields = struct.unpack(">fffBBfIHBB", payload)
    return {
        "processor_temp": fields[0],
        "processor_freq": fields[1],
        "processor_util": fields[2],
        "ram_usage": fields[3],
        "disk_usage": fields[4],
        "cooling_fan_speed": fields[5],
        "uptime": fields[6],
        "watchdog_counter": fields[7],
        "software_version": fields[8],
        "event_flags": fields[9],
    }
decoded = decode_ccsds_cdh_payload(payload_temp)
print(decoded)