# Test module for CRC functions using pytest
# This module contains tests for the CRC-CCSDS implementation to ensure correctness and reliability.
from src.ccsds import crc

# test_crc_known_vector checks the CRC-16 on a known test vector
# test_crc_append ensures that the CRC is correctly appended to the data
# test_crc_empty_data checks the behavior of the CRC function when given empty input

def test_crc_known_vector():
    """
    Validate CRC-16 on a known test vector.
    """
    data = b"Hello, CCSDS!"
    expected_crc = 0x0AFF  # from your manual test result
    computed_crc = crc.compute_crc16(data)
    assert computed_crc == expected_crc

def test_crc_append():
    """
    Ensure append_crc returns data plus correct CRC.
    """
    data = b"Hello, CCSDS!"
    crc_appended = crc.append_crc(data)
    # last two bytes should match CRC
    crc_bytes = crc_appended[-2:]
    assert int.from_bytes(crc_bytes, 'big') == crc.compute_crc16(data)
    # data should be preserved at the front
    assert crc_appended[:-2] == data

def test_crc_empty_data():
    """
    Check behavior on empty input.
    """
    data = b""
    computed_crc = crc.compute_crc16(data)
    # CRC of empty string with 0xFFFF init
    assert computed_crc == 0xFFFF
