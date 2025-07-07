from src.subsystems import adcs
from src.ccsds import encoder
import struct

def decode_ccsds_adcs_payload(payload: bytes) -> dict:
    """
    Decode the ADCS payload to verify correctness.
    """
    fields = struct.unpack(">ffffffffff4B", payload)
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

def test_adcs_telemetry_keys():
    """
    Confirm all expected ADCS telemetry keys are present.
    """
    data = adcs.get_adcs_telemetry()
    expected_keys = [
        "quat_w",
        "quat_x",
        "quat_y",
        "quat_z",
        "ang_velocity_x",
        "ang_velocity_y",
        "ang_velocity_z",
        "mag_field_x",
        "mag_field_y",
        "mag_field_z",
        "sun_sensor_status",
        "gyro_status",
        "adcs_mode",
        "adcs_fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_adcs_payload_encoding_decoding():
    """
    Validate the ADCS payload round-trip through the encoder and decoder.
    """
    data = adcs.get_adcs_telemetry()
    payload = encoder.encode_ccsds_adcs_payload(data)
    decoded = decode_ccsds_adcs_payload(payload)

    # approximate float checks
    for field in [
        "quat_w",
        "quat_x",
        "quat_y",
        "quat_z",
        "ang_velocity_x",
        "ang_velocity_y",
        "ang_velocity_z",
        "mag_field_x",
        "mag_field_y",
        "mag_field_z"
    ]:
        assert abs(decoded[field] - data[field]) < 0.01

    # exact for integers
    assert decoded["sun_sensor_status"] == data["sun_sensor_status"]
    assert decoded["gyro_status"] == data["gyro_status"]
    assert decoded["adcs_mode"] == data["adcs_mode"]
    assert decoded["adcs_fault_flags"] == data["adcs_fault_flags"]

def test_adcs_payload_length():
    """
    Confirm the payload is the expected length:
    10 floats (4 bytes each) +
    4 uint8 (1 byte each)
    = 10*4 + 4 = 44 bytes
    """
    data = adcs.get_adcs_telemetry()
    payload = encoder.encode_ccsds_adcs_payload(data)
    assert len(payload) == 44
