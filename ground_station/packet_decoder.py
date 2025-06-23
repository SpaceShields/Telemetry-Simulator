import struct
from datetime import datetime, timezone

def decode_primary_header(packet: bytes) -> dict:
    version_type_apid, seq_flags_count, length = struct.unpack('>HHH', packet[:6])
    version = (version_type_apid >> 13) & 0x07
    pkt_type = (version_type_apid >> 12) & 0x01
    sec_hdr_flag = (version_type_apid >> 11) & 0x01
    seq_flags = (seq_flags_count >> 14) & 0x03
    seq_count = seq_flags_count & 0x3FFF
    apid = version_type_apid & 0x07FF

    if len(packet) != 38:
        raise ValueError("Invalid CCSDS packet length")

    return {
        "version": version,
        "pkt_type": pkt_type,
        "sec_hdr_flag": sec_hdr_flag,
        "apid": apid,
        "seq_flags": seq_flags,
        "seq_count": seq_count,
        "length": length + 1
    }

def decode_secondary_header(packet: bytes) -> dict:
    timestamp = struct.unpack('>I', packet[6:10])[0]
    return {
        "timestamp": datetime.fromtimestamp(timestamp).isoformat()
    }

def decode_payload(packet: bytes) -> dict:
    payload = struct.unpack('>ffffffI', packet[10:38])
    return {
        "cpu_temp": payload[0],
        "cpu_freq": payload[1],
        "cpu_usage": payload[2],
        "ram": payload[3],
        "disk_usage": payload[4],
        "fan_speed": payload[5],
        "uptime": payload[6]
    }

def decode_ccsds_packet(packet: bytes) -> dict:
    primary = decode_primary_header(packet)
    secondary = decode_secondary_header(packet)
    payload = decode_payload(packet)
    return {
        "primary": primary,
        "secondary": secondary,
        "payload": payload
    }

def print_decoded_packet(decoded: dict):
    print("\n=== [CCSDS PACKET RECEIVED] ===", flush=True)

    print("[PRIMARY HEADER]", flush=True)
    for k, v in decoded["primary"].items():
        print(f"  {k:<18}: {v}", flush=True)

    print("\n[SECONDARY HEADER]", flush=True)
    for k, v in decoded["secondary"].items():
        print(f"  {k:<15}: {v}", flush=True)

    print("\n[PAYLOAD]", flush=True)
    payload = decoded["payload"]
    print(f"  CPU Temp          : {payload['cpu_temp']:.2f} C", flush=True)
    print(f"  CPU Frequency     : {payload['cpu_freq']:.2f} MHz", flush=True)
    print(f"  CPU Usage         : {payload['cpu_usage']:.2f} %", flush=True)
    print(f"  RAM Usage         : {payload['ram']:.2f} %", flush=True)
    print(f"  Disk Usage        : {payload['disk_usage']:.2f} %", flush=True)
    print(f"  Fan Speed         : {payload['fan_speed']:.2f} RPM", flush=True)
    
    # Convert uptime to HH:MM:SS
    uptime_sec = payload["uptime"]
    hrs, rem = divmod(uptime_sec, 3600)
    mins, secs = divmod(rem, 60)
    print(f"  Uptime            : {int(hrs):02}:{int(mins):02}:{int(secs):02}", flush=True)

    print("=" * 40, flush=True)