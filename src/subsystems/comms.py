import random

def get_comms_telemetry():
    """
    Simulates communications telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated communications telemetry data.
    """
    # S-band nominal
    tx_nominal = 2250.0  # MHz
    rx_nominal = 2200.0  # MHz

    # apply small random offset
    tx_frequency = round(tx_nominal + random.uniform(-0.01, 0.01), 6)
    rx_frequency = round(rx_nominal + random.uniform(-0.01, 0.01), 6)

    tx_power = round(random.uniform(0, 30), 2) # dBm
    rx_signal_strength = round(random.uniform(-120, 0), 2) # dBm
    bit_error_rate = round(random.uniform(0, 1e-3), 8) # BER
    frame_sync_errors = random.randint(0, 65535) # count of sync errors
    carrier_lock = random.choice([0, 1]) # boolean
    # Mod types 0-3 (0 = FSK, 1 = BPSK, 2 = QPSK, 3 = 16-QAM)
    # Will stay as BPSK for now, but can be extended later
    modulation_mode = 1 # modulation type
    # Comm modes 0-4 (0 = idle, 1 = normal, 2 = safe, 3 = emergency, 4 = recovery)
    comms_mode = 1 # normal mode
    comms_fault_flags = random.randint(0, 255) # bitfield for faults

    return {
        "tx_frequency": tx_frequency,
        "rx_frequency": rx_frequency,
        "tx_power": tx_power,
        "rx_signal_strength": rx_signal_strength,
        "bit_error_rate": bit_error_rate,
        "frame_sync_errors": frame_sync_errors,
        "carrier_lock": carrier_lock,
        "modulation_mode": modulation_mode,
        "comms_mode": comms_mode,
        "comms_fault_flags": comms_fault_flags
    }