import random

def get_payload_telemetry():
    """
    Simulates payload telemetry data for the spacecraft.
    
    Returns:
        dict: A dictionary containing simulated payload telemetry data.
    """
    camera_status = 1  # Camera status (1 for active, 0 for inactive)
    spectrometer_status = 1  # Spectrometer status (1 for active, 0 for inactive)
    image_capture_count = random.randint(0, 65535)  # Image capture count (0 to 65535)
    last_image_quality = round(random.uniform(0, 100),0)  # Last image quality in percentage
    spectrometer_last_wavelength = round(random.uniform(200.0, 2500.0), 2)  # Last wavelength in nm
    spectrometer_last_intensity = round(random.uniform(0.0, 1000.0), 2)  # Last intensity in arbitrary units
    payload_mode = random.choice([0, 1])  # Payload mode (0 = idle, 1 = survey, 2 = calibration, 3 = emergency)
    payload_fault_flags = 0b00000000  # Healthy state (bitfield)
    
    return {
        "camera_status": camera_status,
        "spectrometer_status": spectrometer_status,
        "image_capture_count": image_capture_count,
        "last_image_quality": last_image_quality,
        "spectrometer_last_wavelength": spectrometer_last_wavelength,
        "spectrometer_last_intensity": spectrometer_last_intensity,
        "payload_mode": payload_mode,
        "payload_fault_flags": payload_fault_flags
    }