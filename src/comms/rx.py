import socket
from src.ccsds.decoder import decode_ccsds_packet
import struct
import pprint

def receive_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            hex_display = ":".join(f"{byte:02X}" for byte in data)
            print(f"[RX] Received {len(data)} bytes from {addr} -> {hex_display}", flush=True)
            print("[RX] Decoding packet...", flush=True)
            print("==========================", flush=True)
            try:
                decoded = decode_ccsds_packet(data)
                pprint.pprint(decoded, sort_dicts=False)
                print(f"[RX] Decoded packet successfully with payload length {len(data)}.", flush=True)
            except (ValueError, struct.error) as e:
                print(f"[RX] Error decoding packet: {e}", flush=True)
                print("===========================", flush=True)
                continue
            print("===========================", flush=True)
    except KeyboardInterrupt:
        print("\n[RX] Shutdown requested. Closing socket...", flush=True)
    finally:
        sock.close()
        print("[RX] Socket closed.", flush=True)