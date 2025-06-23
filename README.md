Absolutely — here’s a **fresh, professional, mission-focused `README.md`** tailored to your CCSDS-based Raspberry Pi telemetry simulator and real-time web dashboard.

---

## 📘 `README.md`

```markdown
# 🛰️ TLI-Telemetry-Simulator

A real-time telemetry simulation framework that emulates spacecraft downlink using CCSDS-compliant packets from a Raspberry Pi-5 "spacecraft" to a mission control ground station dashboard.

Built for rapid prototyping, operator visualization, and low-cost flight-like testing environments.

---

## 🚀 Overview

This project simulates real-time spacecraft telemetry from a Raspberry Pi system using realistic packet encoding, UDP downlink, and a Flask-based mission control dashboard with a modern web interface.

- 🔧 Encodes and transmits CCSDS-formatted packets
- 🧠 Transmits real Pi system telemetry (CPU temp, RAM, fan speed, uptime)
- 📡 Streams data over UDP from spacecraft to ground
- 📊 Decodes and displays live telemetry in a mission-style dashboard
- 🧱 Modular design for extension to multiple subsystems

---

## 📁 Project Structure

```

TLI-Telemetry-Simulator/
├── src/                        # Core packet encoding and Pi telemetry
│   ├── pi\_reader.py
│   ├── packet\_encoder.py
│   └── packet\_decoder.py
│
├── dashboard/                  # Mission control dashboard (Flask)
│   ├── server.py
│   ├── templates/
│   │   └── dashboard.html
│   └── static/                 # Optional: custom CSS/JS
│
├── ground\_station/            # CLI receiver + decoder
│   └── receiver.py
│
├── run\_transmitter.py         # RPi telemetry loop
├── run\_groundstation.py       # CLI receiver loop
├── .env                       # IP/port configuration
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
````

### 2. Add `.env` File

Create a `.env` in the root with:

```env
GROUND_IP=192.168.1.100
GROUND_PORT=5005
```

> Your Pi must send to this IP and port.

---

## 🔄 Usage

### ▶️ Transmit Telemetry from RPi

```bash
python run_transmitter.py
```

### 📡 Receive via CLI

```bash
python run_groundstation.py
```

### 🌐 Run Web Dashboard

```bash
cd dashboard
python server.py
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📦 Packet Format (38 bytes)

| Section          | Length | Details                   |
| ---------------- | ------ | ------------------------- |
| Primary Header   | 6 B    | CCSDS standard            |
| Secondary Header | 4 B    | UNIX timestamp (uint32)   |
| Payload          | 28 B   | 6 floats + 1 int (uptime) |

Payload includes:

* `cpu_temp` (°C), `cpu_freq` (MHz), `cpu_usage` (%)
* `ram` (%), `disk_usage` (%), `fan_speed` (RPM)
* `uptime` (sec, uint32)

---

## ✅ Roadmap

* [ ] Add Chart.js visualization
* [ ] Add APID filtering for subsystems
* [ ] Add logging to CSV/SQLite
* [ ] Add fault injection & alerts

---

## 📜 License

MIT — Use freely for simulation, research, and flight prototyping.

```

---

Let me know if you'd like a version tailored for public open-source distribution or a stripped-down version for internal engineering team use.
```
