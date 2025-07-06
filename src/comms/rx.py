import socket
from src.ccsds.decoder import decode_ccsds_packet, print_decoded_packet

def receive_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            hex_display = ":".join(f"{byte:02X}" for byte in data)
            print(f"[RX] Received {len(data)} bytes from {addr} -> {hex_display}", flush=True)
            print_decoded_packet(decode_ccsds_packet(data))
    except KeyboardInterrupt:
        print("\n[RX] Shutdown requested. Closing socket...", flush=True)
    finally:
        sock.close()
        print("[RX] Socket closed.", flush=True)