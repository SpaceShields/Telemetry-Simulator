"""
Provide a reusable CCSDS secondary header time code

Follow CCSDS 301.0-B guidelines for CUC (CCSDS Unsegmented Time Code)

The CUC typically contains:

    coarse time (seconds since epoch)

    fine time (fractional seconds in smaller units)
"""

from datetime import datetime
import time

# Constants
# CCSDS epoch start date UNIX timestamp
CCSDS_EPOCH = datetime(1970, 1, 1)  # Start of CCSDS epoch

# Simulated mission start time
MISSION_START = datetime(2024, 10, 19, 11, 11, 11)  # Example mission start

# Bit size for coarse and fine time
COARSE_TIME_BITS = 24  # Coarse time in seconds
FINE_TIME_BITS = 8    # Fine time in microseconds or nanoseconds

def encode_cuc_time():
    """    
    Encode the current time into a CCSDS Unsegmented Time Code (CUC).
    Returns:
        bytes: A 4-byte sequence representing the CUC time.
    """
    # Get the current time
    now = time.time()

    # Mission elapsed time since CCSDS epoch
    mission_elapsed = int(now - MISSION_START.timestamp())

    # Split into coarse and fine time
    coarse = mission_elapsed % (2**COARSE_TIME_BITS)  # Coarse time is 24 bits (0 to 16,777,215 seconds)
    fractional = now - int(now)  # Get the fractional part of the current time
    fine = int(fractional * 256)  # Convert to microseconds (1 second = 1,000,000 microseconds) with range 0-255

    # pack the coarse time as a 3-byte big-endian integer
    coarse_bytes = coarse.to_bytes(3, 'big')
    # pack the fine time as a 1-byte big-endian integer
    fine_bytes = int(fine).to_bytes(1, 'big')
    # Combine coarse and fine bytes
    cuc_time = coarse_bytes + fine_bytes

    # Ensure the total length is 4 bytes
    if len(cuc_time) != 4:
        raise ValueError("Encoded CUC time must be 4 bytes long")
    # Return the CUC time as bytes
    return cuc_time

def decode_cuc_time(cuc_time: bytes):
    """
    Decode a CCSDS Unsegmented Time Code (CUC) from bytes.

    Args:
        cuc_time (bytes): The CUC time as a 4-byte sequence.

    Returns:
        tuple: (coarse_time, fine_time) where coarse_time is in seconds and fine_time is in microseconds.
    """
    if len(cuc_time) != 4:
        raise ValueError("CUC time must be exactly 4 bytes long")

    # Extract coarse and fine time
    coarse = int.from_bytes(cuc_time[:3], 'big')  # First 3 bytes for coarse time
    fine = int.from_bytes(cuc_time[3:], 'big')   # Last byte for fine time

    return coarse, fine

def cuc_time_pretty_print(cuc_time: bytes):
    """
    Pretty print the CUC time in a human-readable format.

    Args:
        cuc_time (bytes): The CUC time as a 4-byte sequence.
    """
    coarse, fine = decode_cuc_time(cuc_time)
    print(f"Coarse Time: {coarse} seconds")
    print(f"Fine Time: {fine / 256} seconds")
    print(f"Total Time: {coarse + fine / 1_000_000} seconds since mission start")
