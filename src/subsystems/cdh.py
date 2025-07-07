import psutil
import time

def get_cdh_telemetry():
    """
    Return a dictionary of CDH subsystem telemetry values
    """

    # Read data from the Pi5
    
    # Defensive, fallback-protected metrics
    temps = psutil.sensors_temperatures()
    if temps and 'cpu_thermal' in temps and temps['cpu_thermal']:
        temp = temps['cpu_thermal'][0].current
    else:
        temp = 45.0  # reasonable fallback

    freq = psutil.cpu_freq().current
    util = psutil.cpu_percent()
    ram = int(psutil.virtual_memory().percent)
    disk_usage = int(psutil.disk_usage('/').percent)
    fans = psutil.sensors_fans()
    try:
        fan_speed = next(iter(fans.values()))[0].current if fans else 0.0 
    except (StopIteration, IndexError):
        fan_speed = 0.0
    uptime = int(time.time() - psutil.boot_time())

    # Simulated data
    watchdog_counter = 0  # Placeholder for watchdog counter
    software_version = 1  # Placeholder for software version
    event_flags = 0b00000000  # Placeholder for event flags

    return {
        "processor_temp": temp,
        "processor_freq": freq,
        "processor_util": util,
        "ram_usage": ram,
        "disk_usage": disk_usage,
        "cooling_fan_speed": fan_speed,
        "uptime": uptime,
        "watchdog_counter": watchdog_counter,
        "software_version": software_version,
        "event_flags": event_flags
    }