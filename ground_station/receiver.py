import socket

def receive_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[RX] Received {len(data)} bytes from {addr} → {data.hex()}")