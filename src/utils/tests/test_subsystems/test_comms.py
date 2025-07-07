from src.subsystems import comms
from src.ccsds import encoder, decoder



def test_comms_telemetry_keys():
    """
    Confirm all expected comms telemetry keys are present.
    """
    data = comms.get_comms_telemetry()
    expected_keys = [
        "tx_frequency",
        "rx_frequency",
        "tx_power",
        "rx_signal_strength",
        "bit_error_rate",
        "frame_sync_errors",
        "carrier_lock",
        "modulation_mode",
        "comms_mode",
        "comms_fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_comms_payload_encoding_decoding():
    """
    Validate the comms payload round-trip through the encoder and decoder.
    """
    data = comms.get_comms_telemetry()
    payload = encoder.encode_ccsds_comms_payload(data)
    decoded = decoder.decode_ccsds_comms_payload(payload)

    # approximate float checks
    for field in [
        "tx_frequency",
        "rx_frequency",
        "tx_power",
        "rx_signal_strength",
        "bit_error_rate"
    ]:
        assert abs(decoded[field] - data[field]) < 0.01

    # exact for integers
    assert decoded["frame_sync_errors"] == data["frame_sync_errors"]
    assert decoded["carrier_lock"] == data["carrier_lock"]
    assert decoded["modulation_mode"] == data["modulation_mode"]
    assert decoded["comms_mode"] == data["comms_mode"]
    assert decoded["comms_fault_flags"] == data["comms_fault_flags"]

def test_comms_payload_length():
    """
    Confirm the payload is the expected length:
    5 floats (4 bytes each = 20) +
    1 uint32 (4 bytes) +
    4 uint8 (1 byte each)
    = 20 + 4 + 4 = 28 bytes
    """
    data = comms.get_comms_telemetry()
    payload = encoder.encode_ccsds_comms_payload(data)
    assert len(payload) == 28
