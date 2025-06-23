import struct
from datetime import datetime, timedelta

# # Assume simulation starts at a known datetime (TLI event time, etc.)
# mission_start = datetime(2025, 6, 21, 0, 0, 0)

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

def encode_secondary_header() -> bytes:
    timestamp = int(datetime.now().timestamp())
    return struct.pack('>I', timestamp)

def encode_payload(data: dict) -> bytes:
    return struct.pack(
        ">ffffffI",
        data["cpu_temp"],
        data["cpu_freq"],
        data["cpu_usage"],
        data["ram"],
        data["disk_usage"],
        data["fan_speed"],
        data["uptime"]
    )

def encode_ccsds_packet(data: dict, apid: int, seq_count: int) -> bytes:
    payload = encode_payload(data)
    sec_header = encode_secondary_header()
    packet_length = len(sec_header) + len(payload)
    primary = encode_primary_header(apid, seq_count, packet_length)
    return primary + sec_header + payload
