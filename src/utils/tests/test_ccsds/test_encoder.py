import pytest
from src.ccsds.encoder import encode_ccsds_packet
from src.subsystems import cdh
from src.ccsds import apid

def test_encode_cdh_packet_length_and_structure():
    # Arrange
    data = cdh.get_cdh_telemetry()
    seq_count = 42
    subsystem = "cdh"

    # Act
    packet = encode_ccsds_packet(subsystem, data, seq_count)

    # Expected length:
    # Primary header = 6 bytes
    # Secondary header = 4 bytes
    # CDH payload = 27 bytes (based on CDH_STRUCT_FORMAT)
    # CRC = 2 bytes
    expected_len = 6 + 4 + 26 + 2

    # Assert
    assert isinstance(packet, bytes)
    assert len(packet) == expected_len

    # Check APID embedded (11 bits: bytes 0–1)
    header = packet[:6]
    version_type_secflag_apid = int.from_bytes(header[:2], byteorder="big")
    apid_value = apid.get_apid(subsystem)

    # APID is lower 11 bits
    extracted_apid = version_type_secflag_apid & 0x07FF
    assert extracted_apid == apid_value

    # Check sequence count (bytes 2–3)
    seq_bits = int.from_bytes(header[2:4], byteorder="big")
    extracted_seq_count = seq_bits & 0x3FFF
    assert extracted_seq_count == seq_count
