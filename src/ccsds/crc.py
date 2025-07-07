# Purpose of this file: This file contains the implementation of the CRC-CCSDS algorithm.
# Provide a reusable CRC calculation to append a checksum to each CCSDS packet.
# CCSDS standards often use a 16-bit CRC (CRC-16-CCITT) or a Reed-Solomon code on the transfer frame
# For packet-level validation, a simple 16-bit CRC is sufficient.

# Polynomial: x^16 + x^12 + x^5 + 1 (0x1021)

def compute_crc16(data: bytes) -> int:
    """
    Compute the CRC-16-CCITT checksum for the given data.
    
    Args:
        data (bytes): The input data to compute the CRC for.
        
    Returns:
        int: The computed CRC-16-CCITT checksum.
    """
    crc = 0xFFFF  # Initial value
    for byte in data:
        crc ^= byte << 8  # XOR byte into high byte of crc
        for _ in range(8):  # Process each bit
            if crc & 0x8000:  # If the high bit is set
                crc = (crc << 1) ^ 0x1021  # Shift left and XOR with polynomial
            else:
                crc <<= 1  # Just shift left
            crc &= 0xFFFF  # Ensure crc remains a 16-bit value
    return crc

def append_crc(data: bytes) -> bytes:
    """
    Append the CRC-16-CCITT checksum to the given data.
    
    Args:
        data (bytes): The input data to append the CRC to.
        
    Returns:
        bytes: The input data with the CRC-16-CCITT checksum appended.
    """
    crc = compute_crc16(data)
    crc_bytes = crc.to_bytes(2, byteorder='big')  # Convert CRC to 2 bytes
    return data + crc_bytes
 