from src.subsystems import thermal
from src.ccsds import encoder
import struct

def decode_ccsds_thermal_payload(payload: bytes) -> dict:
    """
    Decode the thermal payload to verify correctness.
    """
    fields = struct.unpack(">fBBBBffB", payload)
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

def test_thermal_telemetry_keys():
    """
    Confirm all expected thermal telemetry keys are present.
    """
    data = thermal.get_thermal_telemetry()
    expected_keys = [
        "average_temp",
        "heater_status",
        "radiator_status",
        "heat_pipe_status",
        "thermal_mode",
        "hot_spot_temp",
        "cold_spot_temp",
        "thermal_fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_thermal_payload_encoding_decoding():
    """
    Validate the thermal payload round-trip through the encoder and decoder.
    """
    data = thermal.get_thermal_telemetry()
    payload = encoder.encode_ccsds_thermal_payload(data)
    decoded = decode_ccsds_thermal_payload(payload)

    # approximate float checks
    for field in [
        "average_temp",
        "hot_spot_temp",
        "cold_spot_temp"
    ]:
        assert abs(decoded[field] - data[field]) < 0.5

    # exact for integers
    assert decoded["heater_status"] == data["heater_status"]
    assert decoded["radiator_status"] == data["radiator_status"]
    assert decoded["heat_pipe_status"] == data["heat_pipe_status"]
    assert decoded["thermal_mode"] == data["thermal_mode"]
    assert decoded["thermal_fault_flags"] == data["thermal_fault_flags"]

def test_thermal_payload_length():
    """
    Confirm the payload is the expected length:
    3 floats (4 bytes each) +
    5 uint8 (1 byte each)
    = 3*4 + 5*1 = 12 + 5 = 17 bytes
    """
    data = thermal.get_thermal_telemetry()
    payload = encoder.encode_ccsds_thermal_payload(data)
    assert len(payload) == 17
