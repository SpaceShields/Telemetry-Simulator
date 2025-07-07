import socket
import time
from collections import defaultdict
from src.ccsds.encoder import encode_ccsds_packet
from src.subsystems import adcs, cdh, comms, payload, power, propulsion, thermal
from dotenv import load_dotenv
import os

load_dotenv()

GROUND_IP = os.getenv("GROUND_IP", "127.0.0.1")  # default localhost
GROUND_PORT = int(os.getenv("GROUND_PORT", 5005))

SCHEDULE = {
    'cdh': 1,
    'power': 0.5,
    'thermal': 0.2,
    'comms': 1,
    'adcs': 2,
    'propulsion': 0.1,
    'payload': 0.2
}

GET_TELEMETRY_FUNC = {
    'cdh': cdh.get_cdh_telemetry,
    'power': power.get_power_telemetry,
    'comms': comms.get_comms_telemetry,
    'thermal': thermal.get_thermal_telemetry,
    'adcs': adcs.get_adcs_telemetry,
    'propulsion': propulsion.get_propulsion_telemetry,
    'payload': payload.get_payload_telemetry
}

last_emit = {s: 0 for s in SCHEDULE}
seq_count = defaultdict(int)

def transmit_packets(ip=GROUND_IP, port=GROUND_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:

            # Get the current time
            now = time.time()

            # Check each subsystem's schedule
            # If enough time has passed since the last emission, send a packet
            # and update the last_emit time
            for subsystem, rate in SCHEDULE.items():
                # Calculate the interval based on the rate
                interval = 1/rate
                # Check if it's time to emit a packet for this subsystem
                if now - last_emit[subsystem] >= interval:
                    data = GET_TELEMETRY_FUNC[subsystem]() # Get telemetry data for the subsystem
                    packet = encode_ccsds_packet(subsystem, data, seq_count[subsystem]) # Encode the packet
                    sock.sendto(packet, (ip, port)) # Send the packet to the ground station
                    print(f"[TX] Sent to {ip} -> {subsystem.upper()} Packet #{seq_count[subsystem]}") # Print the packet details
                    seq_count[subsystem] = (seq_count[subsystem] + 1) % 16384 # Increment sequence count, wrap around at 16384
                    last_emit[subsystem] = now # Update the last emit time for this subsystem
            time.sleep(0.01)  # Prevent busy-waiting
            
    except KeyboardInterrupt:
        print("\n[TX] Shutdown requested. Closing socket...", flush=True)
    finally:
        sock.close()
        print("[TX] Socket closed.", flush=True)