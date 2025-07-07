from src.subsystems import payload
from src.ccsds import encoder, decoder

def test_payload_telemetry_keys():
    """
    Confirm all expected payload telemetry keys are present.
    """
    data = payload.get_payload_telemetry()
    expected_keys = [
        "camera_status",
        "spectrometer_status",
        "image_capture_count",
        "last_image_quality",
        "spectrometer_last_wavelength",
        "spectrometer_last_intensity",
        "payload_mode",
        "payload_fault_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_payload_payload_encoding_decoding():
    """
    Validate the payload subsystem round-trip through the encoder and decoder.
    """
    data = payload.get_payload_telemetry()
    encoded = encoder.encode_ccsds_payload_payload(data)
    decoded = decoder.decode_ccsds_payload_payload(encoded)

    # approximate float checks
    for field in [
        "spectrometer_last_wavelength",
        "spectrometer_last_intensity"
    ]:
        assert abs(decoded[field] - data[field]) < 0.01

    # integers exact
    for field in [
        "camera_status",
        "spectrometer_status",
        "image_capture_count",
        "last_image_quality",
        "payload_mode",
        "payload_fault_flags"
    ]:
        assert decoded[field] == data[field]

def test_payload_payload_length():
    """
    Confirm the payload size:
    2 floats = 8
    1 uint16 = 2
    5 uint8 = 5
    = 15 bytes total
    """
    data = payload.get_payload_telemetry()
    encoded = encoder.encode_ccsds_payload_payload(data)
    assert len(encoded) == 15
