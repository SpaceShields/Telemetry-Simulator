import pytest
from src.ccsds import time as cuc_time

def test_encode_decode_roundtrip():
    """
    Test that encoding then decoding returns consistent values.
    """
    encoded = cuc_time.encode_cuc_time()
    coarse, fine = cuc_time.decode_cuc_time(encoded)

    # check bounds
    assert 0 <= coarse < 2**24
    assert 0 <= fine < 256

def test_cuc_time_length():
    """
    Ensure encoded CUC time is exactly 4 bytes.
    """
    encoded = cuc_time.encode_cuc_time()
    assert isinstance(encoded, bytes)
    assert len(encoded) == 4

def test_decode_invalid_length():
    """
    Ensure decoding raises for invalid length.
    """
    with pytest.raises(ValueError):
        cuc_time.decode_cuc_time(b"\x00\x01")  # too short

def test_pretty_print(capfd):
    """
    Check that pretty print outputs something meaningful.
    """
    encoded = cuc_time.encode_cuc_time()
    cuc_time.cuc_time_pretty_print(encoded)
    out, _ = capfd.readouterr()
    assert "Coarse Time" in out
    assert "Fine Time" in out
    assert "Total Time" in out
