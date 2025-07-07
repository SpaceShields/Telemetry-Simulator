import random

def get_thermal_telemetry():
    """
    Simulates thermal telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated thermal telemetry data.
    """

    # heater_status: 0 = off, 1 = on
    # radiator status : 0 = inactive, 1 = active
    # heat pipe status: 0 = inactive, 1 = active
    # thermal mode: 0 = idle, 1 = nominal, 2 = suvival, 3 = decontam, 4 = emergency

    heater_status = 0  # heater off (0 for off, 1 for on)
    radiator_status = 1  # radiator active (1 for active, 0 for inactive)
    heat_pipe_status = 1  # heat pipe active (1 for active, 0 for inactive)
    thermal_mode = 1  # nominal mode (adjust as needed)
    hot_spot_temp = round(random.uniform(0.0, 100.0), 1)  # Celsius
    cold_spot_temp = round(random.uniform(-100.0, 0.0), 1)  # Celsius
    average_temp = (hot_spot_temp + cold_spot_temp) / 2  # Celsius
    if average_temp < -10 and average_temp > -40:
        heater_status = 1  # turn heater on if average temp is below -10
        radiator_status = 0  # turn radiator off if heater is on
        thermal_mode = 2  # survival mode
    elif average_temp > 30 and average_temp < 60:
        heater_status = 0  # turn heater off if average temp is above 50
        radiator_status = 1  # turn radiator on if heater is off
    elif average_temp <-40 or average_temp > 60:
        thermal_mode = 4  # emergency mode
    thermal_fault_flags = 0b00000000  # healthy

    return {
        "average_temp": average_temp,
        "heater_status": heater_status,
        "radiator_status": radiator_status,
        "heat_pipe_status": heat_pipe_status,
        "thermal_mode": thermal_mode,
        "hot_spot_temp": hot_spot_temp,
        "cold_spot_temp": cold_spot_temp,
        "thermal_fault_flags": thermal_fault_flags
    }