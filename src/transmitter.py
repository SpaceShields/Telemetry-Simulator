import socket
import time
from src.csv_reader import read_csv
from src.packet_encoder import encode_ccsds_packet
from dotenv import load_dotenv
import os

load_dotenv()

GROUND_IP = os.getenv("GROUND_IP", "127.0.0.1")  # default localhost
GROUND_PORT = int(os.getenv("GROUND_PORT", 5005))

def transmit_packets(
    apid=100,
    interval=1.0,
    ip=GROUND_IP,
    port=GROUND_PORT,
    filepath="data/tli_telemetry_mvp.csv"
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csv_data = read_csv(filepath)
    for seq_count,row in enumerate(csv_data):
        packet = encode_ccsds_packet(row, apid, seq_count)
        sock.sendto(packet, (ip, port))
        print(f"[TX] Packet {seq_count} → {ip}:{port} ({len(packet)} bytes)")
        time.sleep(interval)