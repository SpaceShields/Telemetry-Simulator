import struct
from datetime import datetime, timedelta

# Assume simulation starts at a known datetime (TLI event time, etc.)
mission_start = datetime(2025, 6, 21, 0, 0, 0)

def encode_primary_header(apid: int, seq_count: int, payload_length: int) -> bytes:
    version = 0         # 3 bits
    pkt_type = 0        # 1 bit (0 = telemetry)
    sec_hdr_flag = 1    # 1 bit (1 = present)

    first_2_bytes = ((version & 0x07) << 13) | \
                    ((pkt_type & 0x01) << 12) | \
                    ((sec_hdr_flag & 0x01) << 11) | \
                    (apid & 0x07FF)
    
    second_2_bytes = (0b11 << 14) | (seq_count & 0x3FFF)    # Seq flag + count

    third_2_bytes = payload_length - 1  # CCSDS rule: "length = payload - 1"

    return struct.pack('>HHH', first_2_bytes, second_2_bytes, third_2_bytes)

def encode_secondary_header(row: dict) -> bytes:
    rel_seconds = int(row['timestamp'])
    absolute_time = mission_start + timedelta(seconds=rel_seconds)
    timestamp = int(absolute_time.timestamp())
    return struct.pack('>I', timestamp)

def encode_payload(row: dict) -> bytes:
    pass

def encode_ccsds_packet(row: dict, seq_count: int) -> bytes:
    pass

