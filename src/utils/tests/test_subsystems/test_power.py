from src.subsystems import power
from src.ccsds import encoder, decoder

def test_power_telemetry_keys():
    """
    Confirm all expected power telemetry keys are present.
    """
    data = power.get_power_telemetry()
    expected_keys = [
        "bus_voltage",
        "bus_current",
        "battery_voltage",
        "battery_current",
        "battery_temp",
        "state_of_charge",
        "solar_array_current",
        "solar_array_voltage",
        "eps_mode",
        "fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_power_payload_encoding_decoding():
    """
    Validate the power payload round-trip through the encoder and decoder.
    """
    data = power.get_power_telemetry()
    payload = encoder.encode_ccsds_power_payload(data)
    decoded = decoder.decode_ccsds_power_payload(payload)

    # approximate float checks
    for field in [
        "bus_voltage",
        "bus_current",
        "battery_voltage",
        "battery_current",
        "battery_temp",
        "state_of_charge",
        "solar_array_current",
        "solar_array_voltage"
    ]:
        assert abs(decoded[field] - data[field]) < 0.5

    # exact for uint8
    assert decoded["eps_mode"] == data["eps_mode"]
    assert decoded["fault_flags"] == data["fault_flags"]

def test_power_payload_length():
    """
    Confirm the payload is the expected length:
    8 floats (4 bytes each) + 2 uint8 (1 byte each)
    = 8*4 + 2*1 = 34 bytes
    """
    data = power.get_power_telemetry()
    payload = encoder.encode_ccsds_power_payload(data)
    assert len(payload) == 34