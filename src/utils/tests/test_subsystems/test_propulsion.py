from src.subsystems import propulsion
from src.ccsds import encoder, decoder

def test_propulsion_telemetry_keys():
    """
    Confirm all expected propulsion telemetry keys are present.
    """
    data = propulsion.get_propulsion_telemetry()
    expected_keys = [
        "fuel_level",
        "oxidizer_level",
        "tank_pressure",
        "feedline_temp",
        "valve_status",
        "thruster_firing",
        "thruster_mode",
        "propulsion_fault_flags",
        "rcs_tank_level",
        "rcs_tank_pressure",
        "rcs_thruster_status",
        "rcs_fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_propulsion_payload_encoding_decoding():
    """
    Validate the propulsion payload round-trip through the encoder and decoder.
    """
    data = propulsion.get_propulsion_telemetry()
    payload = encoder.encode_ccsds_propulsion_payload(data)
    decoded = decoder.decode_ccsds_propulsion_payload(payload)

    # floats, allow small differences
    for field in [
        "fuel_level",
        "oxidizer_level",
        "tank_pressure",
        "feedline_temp",
        "rcs_tank_level",
        "rcs_tank_pressure"
    ]:
        assert abs(decoded[field] - data[field]) < 0.01

    # exact matches for status fields
    for field in [
        "valve_status",
        "thruster_firing",
        "thruster_mode",
        "propulsion_fault_flags",
        "rcs_thruster_status",
        "rcs_fault_flags"
    ]:
        assert decoded[field] == data[field]

def test_propulsion_payload_length():
    """
    Confirm the payload is the expected length:
    6 floats (4 bytes each) +
    4 uint8 (1 byte each) +
    2 floats (4 bytes each) +
    2 uint8 (1 byte each)
    = 6*4 + 6*1 = 24 + 6 = 30 bytes
    """
    data = propulsion.get_propulsion_telemetry()
    payload = encoder.encode_ccsds_propulsion_payload(data)
    assert len(payload) == 30
