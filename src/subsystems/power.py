import random

def get_power_telemetry():
    """
    Simulates power telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated power telemetry data.
    """
    bus_voltage = round(random.uniform(26.0, 29.0), 2)  # Volts
    bus_current = round(random.uniform(0.5, 12.0), 2)  # Amps

    # Simulate battery metrics
    battery_voltage = round(random.uniform(24.0, 29.4), 2)
    battery_current = round(random.uniform(-5.0, 5.0), 2)  # charge/discharge
    battery_temp = round(random.uniform(0.0, 35.0), 1)
    state_of_charge = round(random.uniform(30.0, 100.0), 1)

    # Simulate solar array
    solar_array_current = round(random.uniform(0.0, 8.0), 2)
    solar_array_voltage = round(random.uniform(26.0, 29.0), 2)

    # Mode and fault
    # EPS Mode (uint8, 0–5)
        # 0 = off
        # 1 = nominal
        # 2 = safe
        # 3 = charging only
        # 4 = survival mode
        # 5 = emergency
    eps_mode = 1  # nominal mode (adjust as needed)
    fault_flags = 0b00000000  # healthy

    return {
        "bus_voltage": bus_voltage,
        "bus_current": bus_current,
        "battery_voltage": battery_voltage,
        "battery_current": battery_current,
        "battery_temp": battery_temp,
        "state_of_charge": state_of_charge,
        "solar_array_current": solar_array_current,
        "solar_array_voltage": solar_array_voltage,
        "eps_mode": eps_mode,
        "fault_flags": fault_flags
    }