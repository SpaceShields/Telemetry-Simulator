from src.ccsds.encoder import encode_ccsds_packet
from src.ccsds.decoder import decode_ccsds_packet
from src.subsystems import cdh

def test_decode_ccsds_packet_cdh():
    # Generate simulated telemetry
    original_data = cdh.get_cdh_telemetry()
    seq_count = 42

    # Encode into CCSDS packet
    packet = encode_ccsds_packet("cdh", original_data, seq_count)

    # Decode the packet
    decoded = decode_ccsds_packet(packet)

    # Assertions
    assert decoded["primary"]["apid"] == 0x01  # CDH APID
    assert decoded["primary"]["seq_count"] == seq_count
    assert decoded["secondary"]["timestamp"] is not None
    assert isinstance(decoded["secondary"]["timestamp"], str)

    payload = decoded["payload"]
    assert abs(payload["processor_temp"] - original_data["processor_temp"]) < 0.5
    assert abs(payload["processor_freq"] - original_data["processor_freq"]) < 0.5
    assert abs(payload["processor_util"] - original_data["processor_util"]) < 0.5
    assert payload["ram_usage"] == original_data["ram_usage"]
    assert payload["disk_usage"] == original_data["disk_usage"]
    assert abs(payload["cooling_fan_speed"] - original_data["cooling_fan_speed"]) < 10
    assert payload["uptime"] == original_data["uptime"]
    assert payload["software_version"] == original_data["software_version"]
    assert payload["event_flags"] == original_data["event_flags"]
