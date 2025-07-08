import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
from threading import Thread

from src.ccsds.decoder import decode_ccsds_packet
from src.ccsds.apid import get_subsystem


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5005))

    while True:
        data, addr = sock.recvfrom(1024)
        decoded = decode_ccsds_packet(data)
        if not decoded:
            print(f"[RX] Error decoding packet from {addr}. Data: {data}")
            continue

        json_packet = {
            "subsystem": get_subsystem(decoded["primary"]["apid"]).upper(),
            "timestamp": decoded["secondary"]["timestamp"],
            "status": "nominal",
            "sequence_count": decoded["primary"]["seq_count"],
            "data": decoded["payload"]
        }

        socketio.emit('telemetry-details', json_packet, namespace=f'/{json_packet["subsystem"].lower()}')
        socketio.emit('telemetry', json_packet, namespace="/")

udp_thread = Thread(target=udp_listener)
udp_thread.daemon = True
udp_thread.start()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
