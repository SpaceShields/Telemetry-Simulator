import struct
from datetime import datetime

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

PAYLOAD_LENGTHS = {
    0x01: 26,  # CDH
    0x02: 34,  # Power
    0x03: 28,  # Comms
    0x04: 17,  # Thermal
    0x05: 44,  # ADCS
    0x06: 30,  # Propulsion
    0x07: 15   # Payload
}

def decode_ccsds_adcs_payload(payload: bytes) -> dict:
    """
    Decode the ADCS payload to verify correctness.
    """
    fields = struct.unpack(ADCS_STRUCT_FORMAT, payload)
    return {
        "quat_w": fields[0],
        "quat_x": fields[1],
        "quat_y": fields[2],
        "quat_z": fields[3],
        "ang_velocity_x": fields[4],
        "ang_velocity_y": fields[5],
        "ang_velocity_z": fields[6],
        "mag_field_x": fields[7],
        "mag_field_y": fields[8],
        "mag_field_z": fields[9],
        "sun_sensor_status": fields[10],
        "gyro_status": fields[11],
        "adcs_mode": fields[12],
        "adcs_fault_flags": fields[13]
    }

def decode_ccsds_cdh_payload(payload: bytes) -> dict:
    fields = struct.unpack(CDH_STRUCT_FORMAT, payload)
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

def decode_ccsds_comms_payload(payload: bytes) -> dict:
    """
    Decode the comms payload to verify correctness.
    """
    fields = struct.unpack(COMMS_STRUCT_FORMAT, payload)
    return {
        "tx_frequency": fields[0],
        "rx_frequency": fields[1],
        "tx_power": fields[2],
        "rx_signal_strength": fields[3],
        "bit_error_rate": fields[4],
        "frame_sync_errors": fields[5],
        "carrier_lock": fields[6],
        "modulation_mode": fields[7],
        "comms_mode": fields[8],
        "comms_fault_flags": fields[9]
    }

def decode_ccsds_payload_payload(payload_bytes: bytes) -> dict:
    """
    Decode the payload subsystem data for verification.
    """
    fields = struct.unpack(PAYLOAD_STRUCT_FORMAT, payload_bytes)
    return {
        "camera_status": fields[0],
        "spectrometer_status": fields[1],
        "image_capture_count": fields[2],
        "last_image_quality": fields[3],
        "spectrometer_last_wavelength": fields[4],
        "spectrometer_last_intensity": fields[5],
        "payload_mode": fields[6],
        "payload_fault_flags": fields[7]
    }

def decode_ccsds_power_payload(payload: bytes) -> dict:
    """
    Decode the power payload to verify correctness.
    """
    fields = struct.unpack(POWER_STRUCT_FORMAT, payload)
    return {
        "bus_voltage": fields[0],
        "bus_current": fields[1],
        "battery_voltage": fields[2],
        "battery_current": fields[3],
        "battery_temp": fields[4],
        "state_of_charge": fields[5],
        "solar_array_current": fields[6],
        "solar_array_voltage": fields[7],
        "eps_mode": fields[8],
        "fault_flags": fields[9]
    }

def decode_ccsds_propulsion_payload(payload: bytes) -> dict:
    """
    Decode the propulsion payload to verify correctness.
    """
    fields = struct.unpack(PROPULSION_STRUCT_FORMAT, payload)
    return {
        "fuel_level": fields[0],
        "oxidizer_level": fields[1],
        "tank_pressure": fields[2],
        "feedline_temp": fields[3],
        "valve_status": fields[4],
        "thruster_firing": fields[5],
        "thruster_mode": fields[6],
        "propulsion_fault_flags": fields[7],
        "rcs_tank_level": fields[8],
        "rcs_tank_pressure": fields[9],
        "rcs_thruster_status": fields[10],
        "rcs_fault_flags": fields[11]
    }

def decode_ccsds_thermal_payload(payload: bytes) -> dict:
    """
    Decode the thermal payload to verify correctness.
    """
    fields = struct.unpack(THERMAL_STRUCT_FORMAT, payload)
    return {
        "average_temp": fields[0],
        "heater_status": fields[1],
        "radiator_status": fields[2],
        "heat_pipe_status": fields[3],
        "thermal_mode": fields[4],
        "hot_spot_temp": fields[5],
        "cold_spot_temp": fields[6],
        "thermal_fault_flags": fields[7]
    }

DECODE_ROUTER = {
    0x01: decode_ccsds_cdh_payload,
    0x02: decode_ccsds_power_payload,
    0x03: decode_ccsds_comms_payload,
    0x04: decode_ccsds_thermal_payload,
    0x05: decode_ccsds_adcs_payload,
    0x06: decode_ccsds_propulsion_payload,
    0x07: decode_ccsds_payload_payload
}

def decode_payload(packet: bytes, apid: int) -> dict:
    if apid not in DECODE_ROUTER:
        raise ValueError(f"Unsupported APID: {apid}")
    
    expected_len = PAYLOAD_LENGTHS[apid]
    actual_payload = packet[10:-2]

    if len(actual_payload) != expected_len:
        raise ValueError(f"[DECODE ERROR] APID {apid:#04x}: Expected {expected_len} bytes, got {len(actual_payload)} bytes")
    
    return DECODE_ROUTER[apid](actual_payload)

def decode_primary_header(packet: bytes) -> dict:
    version_type_apid, seq_flags_count, length = struct.unpack('>HHH', packet[:6])
    version = (version_type_apid >> 13) & 0x07
    pkt_type = (version_type_apid >> 12) & 0x01
    sec_hdr_flag = (version_type_apid >> 11) & 0x01
    seq_flags = (seq_flags_count >> 14) & 0x03
    seq_count = seq_flags_count & 0x3FFF
    apid = version_type_apid & 0x07FF

    # Extract length field from header (already unpacked above)
    expected_packet_length = length + 1 + 6  # +1 as per CCSDS standard, +6 for primary header
    if len(packet) < expected_packet_length:
        raise ValueError(f"Incomplete CCSDS packet. Expected {expected_packet_length}, got {len(packet)}")
    
    return {
        "version": version,
        "pkt_type": pkt_type,
        "sec_hdr_flag": sec_hdr_flag,
        "apid": apid,
        "seq_flags": seq_flags,
        "seq_count": seq_count,
        "length": length + 1
    }

def decode_secondary_header(packet: bytes) -> dict:
    timestamp = struct.unpack('>I', packet[6:10])[0]
    return {
        "timestamp": datetime.fromtimestamp(timestamp).isoformat()
    }

def decode_ccsds_packet(packet: bytes) -> dict:
    primary = decode_primary_header(packet)
    secondary = decode_secondary_header(packet)
    payload = decode_payload(packet, primary["apid"])

    if len(packet) != 34:  # or use struct.calcsize(format)
        raise ValueError(f"[DECODE ERROR] APID 0x03: Expected 34 bytes, got {len(packet)}")

    return {
        "primary": primary,
        "secondary": secondary,
        "payload": payload
    }