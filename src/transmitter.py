import socket
import time
from src.csv_reader import read_csv
from src.packet_encoder import encode_ccsds_packet

def transmit_packets(
    apid=100,
    interval=1.0,
    ip="192.168.1.10",
    port=5005,
    filepath="data/tli_telemetry_mvp.csv"
):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    csv_data = read_csv(filepath)
    for seq_count,row in enumerate(csv_data):
        packet = encode_ccsds_packet(row, apid, seq_count)
        sock.sendto(packet, (ip, port))
        print(f"[TX] Packet {seq_count} → {ip}:{port} ({len(packet)} bytes)")
        time.sleep(interval)