import random

def get_adcs_telemetry():
    """
    Simulates ADCS telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated ADCS telemetry data.
    """
    # Quaternion components (w, x, y, z) for attitude representation
    # Values are rounded to 6 decimal places for precision
    quat_w = round(random.uniform(-1.0, 1.0), 6)  # Quaternion w component
    quat_x = round(random.uniform(-1.0, 1.0), 6)  # Quaternion x component
    quat_y = round(random.uniform(-1.0, 1.0), 6)  # Quaternion y component
    quat_z = round(random.uniform(-1.0, 1.0), 6)  # Quaternion z component

    # Angular velocity components (x, y, z) in degrees per second
    # Values are rounded to 1 decimal place for precision
    ang_velocity_x = round(random.uniform(-5.0, 5.0), 1)  # Angular velocity x component
    ang_velocity_y = round(random.uniform(-5.0, 5.0), 1)  # Angular velocity y component
    ang_velocity_z = round(random.uniform(-5.0, 5.0), 1)  # Angular velocity z component

    # Magnetic field components (x, y, z) in microteslas
    # Values are rounded to 1 decimal place for precision
    mag_field_x = round(random.uniform(-60.0, 60.0), 1)  # Magnetic field x component
    mag_field_y = round(random.uniform(-60.0, 60.0), 1)  # Magnetic field y component
    mag_field_z = round(random.uniform(-60.0, 60.0), 1)  # Magnetic field z component

    # Simulated statuses and modes
    sun_sensor_status = 1  # Sun sensor status (1 for active, 0 for inactive)
    gyro_status = 1  # Gyro status (1 for active, 0 for inactive)
    adcs_mode = 3 # ADCS mode (0 = idle, 1 = detumble, 2 = coarse point, 3 = fine point, 4 = emergency)
    adcs_fault_flags = 0b00000000  # Healthy state (bitfield)

    return {
        "quat_w": quat_w,
        "quat_x": quat_x,
        "quat_y": quat_y,
        "quat_z": quat_z,
        "ang_velocity_x": ang_velocity_x,
        "ang_velocity_y": ang_velocity_y,
        "ang_velocity_z": ang_velocity_z,
        "mag_field_x": mag_field_x,
        "mag_field_y": mag_field_y,
        "mag_field_z": mag_field_z,
        "sun_sensor_status": sun_sensor_status,
        "gyro_status": gyro_status,
        "adcs_mode": adcs_mode,
        "adcs_fault_flags": adcs_fault_flags
    }