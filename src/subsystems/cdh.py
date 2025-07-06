import psutil
import time
import os

def read_pi_data():
    cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current  # or custom
    cpu_freq = psutil.cpu_freq().current
    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    fans = psutil.sensors_fans()
    fan_speed = next(iter(fans.values()))[0].current if fans else 0.0 
    uptime = int(time.time() - psutil.boot_time())

    cpu_temp = round(cpu_temp, 2)
    cpu_freq = round(cpu_freq, 1)
    cpu_usage = round(cpu_usage, 1)

    return {
        "cpu_temp": cpu_temp,
        "cpu_freq": cpu_freq,
        "cpu_usage": cpu_usage,
        "ram": ram,
        "disk_usage": disk_usage,
        "fan_speed": fan_speed,
        "uptime": uptime
    }