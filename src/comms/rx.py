import socket
from src.ccsds.decoder import decode_ccsds_packet

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
                decoded_data = decode_ccsds_packet(data)
                print(decoded_data, flush=True)
                print("[RX] Decoded packet successfully.", flush=True)
            except ValueError as e:
                print(f"[RX] Error decoding packet: {e}", flush=True)
                continue
            print("===========================", flush=True)
    except KeyboardInterrupt:
        print("\n[RX] Shutdown requested. Closing socket...", flush=True)
    finally:
        sock.close()
        print("[RX] Socket closed.", flush=True)