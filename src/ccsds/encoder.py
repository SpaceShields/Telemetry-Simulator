import struct
from src.ccsds import time, crc, apid

"""
Purpose of this file: This file contains the implementation of the CCSDS encoder.
It provides functions to encode CCSDS packets, including adding APID, CUC time, and CRC.
The encoder ensures that the packets conform to the CCSDS standards for data transfer.
CCSDS 133.0-B (telemetry source packets)
"""

# define the struct format
# >: big-endian
# f: float (4 bytes)
# I: uint32 (4 bytes)
# H: uint16 (2 bytes)
# B: uint8 (1 byte)
CDH_STRUCT_FORMAT = ">fffBBfIHBB" # bytes = 26 (total w/headers and CRC = 38)
POWER_STRUCT_FORMAT = ">ffffffffBB" # bytes = 34 (total w/headers and CRC = 46)
COMMS_STRUCT_FORMAT = ">fffffI4B" # bytes = 28 (total w/headers and CRC = 40)
THERMAL_STRUCT_FORMAT = ">fBBBBffB" # bytes = 17 (total w/headers and CRC = 29)
ADCS_STRUCT_FORMAT = ">ffffffffff4B" # bytes = 44 (total w/headers and CRC = 56)
PROPULSION_STRUCT_FORMAT = ">ffff4BffBB" # bytes = 30 (total w/headers and CRC = 42)
PAYLOAD_STRUCT_FORMAT = ">BBHBffBB" # bytes = 15 (total w/headers and CRC = 27)

# Header constants
CCSDS_VERSION = 0
CCSDS_PKT_TYPE = 0
CCSDS_SEC_HDR_FLAG = 1
CCSDS_SEQ_FLAGS = 0b11


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

def encode_ccsds_payload_payload(data: dict) -> bytes:
    """
    Encodes the telemetry data for the spacecraft surveying and spectrometer payload into a CCSDS-compliant payload based on the subsystem type.

    The struct format is:
        camera_status          -> uint8
        spectrometer_status    -> uint8
        image_capture_count    -> uint16
        last_image_quality     -> uint8
        spectrometer_last_wavelength -> float
        spectrometer_last_intensity -> float
        payload_mode           -> uint8
        payload_fault_flags    -> uint8
    """
    camera_status = int(data['camera_status'])  # 0 or 1
    spectrometer_status = int(data['spectrometer_status'])  # 0 or 1
    image_capture_count = int(data['image_capture_count'])  # 0–65535
    last_image_quality = int(data['last_image_quality'])  # 0.0–100.0
    spectrometer_last_wavelength = float(data['spectrometer_last_wavelength'])  # in nm
    spectrometer_last_intensity = float(data['spectrometer_last_intensity'])  # in arbitrary units
    payload_mode = int(data['payload_mode'])  # 0–3
    payload_fault_flags = int(data['payload_fault_flags'])  # bitfield, 0

    # pack it all in one shot
    payload = struct.pack(
        PAYLOAD_STRUCT_FORMAT,
        camera_status,
        spectrometer_status,
        image_capture_count,
        last_image_quality,
        spectrometer_last_wavelength,
        spectrometer_last_intensity,
        payload_mode,
        payload_fault_flags
        )
    
    return payload

def encode_ccsds_primary_header(apid: int, seq_count: int, total_data_length: int) -> bytes:
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

    first_two_bytes = (
        (CCSDS_VERSION << 13) |  # version (3 bits)
        (CCSDS_PKT_TYPE << 12) |  # type (1 bit)
        (CCSDS_SEC_HDR_FLAG << 11) |  # secondary header flag (1 bit)
        apid  # APID (11 bits)
    )

    second_two_bytes = (
        (CCSDS_SEQ_FLAGS & 0b11) << 14 |  # sequence flags (2 bits)
        (seq_count & 0x3FFF)  # sequence count (14 bits)
    )

    third_two_bytes = total_data_length

    return struct.pack(
        ">HHH",
        first_two_bytes,
        second_two_bytes,
        third_two_bytes
    )

def encode_ccsds_secondary_header() -> bytes:
    """
    use encode_cuc_time() from time.py

    4 bytes

    integrate directly without hardcoding
    """
    return time.encode_cuc_time()

# Dispatch table: maps subsystem → (encoder_fn, apid_key)
subsystem_map = {
    'cdh': (encode_ccsds_cdh_payload, 'cdh'),
    'power': (encode_ccsds_power_payload, 'power'),
    'comms': (encode_ccsds_comms_payload, 'comms'),
    'thermal': (encode_ccsds_thermal_payload, 'thermal'),
    'adcs': (encode_ccsds_adcs_payload, 'adcs'),
    'propulsion': (encode_ccsds_propulsion_payload, 'propulsion'),
    'payload': (encode_ccsds_payload_payload, 'payload'),
}

def encode_ccsds_packet(subsystem: str, data: dict, seq_count: int) -> bytes:
    """
    Encodes a full CCSDS telemetry packet with headers and CRC for a given subsystem.
    """

    if subsystem not in subsystem_map:
        raise ValueError(f"Unknown subsystem: {subsystem}")

    encoder_fn, apid_key = subsystem_map[subsystem]
    payload = encoder_fn(data)
    apid_value = apid.get_apid(apid_key)

    secondary_header = encode_ccsds_secondary_header()

    # Total data field = secondary header + payload, minus 1 (per CCSDS 133.0-B)
    total_data_len = len(secondary_header) + len(payload) - 1
    primary_header = encode_ccsds_primary_header(apid_value, seq_count, total_data_len)

    # Assemble and finalize
    packet = primary_header + secondary_header + payload

    return crc.append_crc(packet)
