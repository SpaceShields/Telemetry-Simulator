import socket
import time
from src.pi_reader import read_pi_data
from src.packet_encoder import encode_ccsds_packet
from dotenv import load_dotenv
import os

load_dotenv()

GROUND_IP = os.getenv("GROUND_IP", "127.0.0.1")  # default localhost
GROUND_PORT = int(os.getenv("GROUND_PORT", 5005))

def transmit_packets(apid=100, interval=1.0, ip=GROUND_IP, port=GROUND_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seq_count = 0 

    while True:
        data = read_pi_data()
        packet = encode_ccsds_packet(data, apid, seq_count)
        sock.sendto(packet, (ip, port))
        hex_display = ":".join(f"{byte:02X}" for byte in packet)
        print(f"[TX] Packet #{seq_count} → {hex_display}")
        seq_count = (seq_count + 1) % 16384
        time.sleep(interval)