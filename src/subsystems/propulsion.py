import random

def get_propulsion_telemetry():
    """
    Simulates propulsion telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated propulsion telemetry data.
    """
    # Simulated propulsion parameters
    fuel_level = round(random.uniform(0.0, 100.0), 2)  # Fuel level in percentage
    oxidizer_level = round(random.uniform(0.0, 100.0), 2)  # Oxidizer level in percentage
    tank_pressure = round(random.uniform(0.0, 30.0), 2)  # Tank pressure in bar
    feedline_temp = round(random.uniform(-40.0, 50.0), 2)  # Feedline temperature in Celsius
    valve_status = 0  # Valve status (0 = closed, 1 = open)
    thruster_firing = 0  # Thruster firing status (0 = not firing, 1 = firing)
    thruster_mode = 0  # Thruster mode (0 = idle, 1 = burn, 2 = coast)
    propulsion_fault_flags = 0b00000000  # Healthy state (bitfield)

    # Reaction Control System (RCS) parameters
    rcs_tank_level = round(random.uniform(0.0, 100.0), 2)  # RCS tank level in percentage
    rcs_tank_pressure = round(random.uniform(0.0, 30.0), 2)  # RCS tank pressure in bar
    rcs_thruster_status = random.choice([0, 1])  # RCS thruster status (0 = inactive, 1 = active)
    rcs_fault_flags = 0b00000000  # Healthy state (bitfield)

    return {
        "fuel_level": fuel_level,
        "oxidizer_level": oxidizer_level,
        "tank_pressure": tank_pressure,
        "feedline_temp": feedline_temp,
        "valve_status": valve_status,
        "thruster_firing": thruster_firing,
        "thruster_mode": thruster_mode,
        "propulsion_fault_flags": propulsion_fault_flags,
        "rcs_tank_level": rcs_tank_level,
        "rcs_tank_pressure": rcs_tank_pressure,
        "rcs_thruster_status": rcs_thruster_status,
        "rcs_fault_flags": rcs_fault_flags
    }