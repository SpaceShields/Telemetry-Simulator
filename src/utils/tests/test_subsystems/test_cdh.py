from src.subsystems import cdh
from src.ccsds import encoder, decoder

# Temporary function to decode the payload

# Test cases for the CDH subsystem telemetry
def test_cdh_telemetry_keys():
    """
    Confirm all expected CDH telemetry keys are present.
    """
    data = cdh.get_cdh_telemetry()
    expected_keys = [
        "processor_temp",
        "processor_freq",
        "processor_util",
        "ram_usage",
        "disk_usage",
        "cooling_fan_speed",
        "uptime",
        "watchdog_counter",
        "software_version",
        "event_flags"
    ]
    for key in expected_keys:
        assert key in data

def test_cdh_payload_encoding_decoding():
    """
    Validate the CDH payload round-trip through the encoder and decoder.
    """
    data = cdh.get_cdh_telemetry()
    payload = encoder.encode_ccsds_cdh_payload(data)
    decoded = decoder.decode_ccsds_cdh_payload(payload)

    # approximate check, float rounding
    assert abs(decoded['processor_temp'] - data['processor_temp']) < 0.5
    assert abs(decoded['processor_freq'] - data['processor_freq']) < 0.5
    assert abs(decoded['processor_util'] - data['processor_util']) < 0.5
    assert decoded['ram_usage'] == int(data['ram_usage'])
    assert decoded['disk_usage'] == int(data['disk_usage'])
    assert abs(decoded['cooling_fan_speed'] - data['cooling_fan_speed']) < 1
    assert decoded['uptime'] == data['uptime']
    assert decoded['watchdog_counter'] == data['watchdog_counter']
    assert decoded['software_version'] == data['software_version']
    assert decoded['event_flags'] == data['event_flags']

def test_cdh_payload_length():
    """
    Confirm the payload is the expected length:
    3 floats (4 bytes each) +
    2 uint8 (1 byte each) +
    1 float (4 bytes) +
    1 uint32 (4 bytes) +
    1 uint16 (2 bytes) +
    2 uint8 (1 byte each)
    = 12 + 2 + 4 + 4 + 2 + 2 = 26 bytes
    """
    data = cdh.get_cdh_telemetry()
    payload = encoder.encode_ccsds_cdh_payload(data)
    assert len(payload) == 26
