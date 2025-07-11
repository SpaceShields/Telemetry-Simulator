# 🛰️ Spacecraft Telemetry Simulator & Mission Control Dashboard

A fully operational MVP that simulates real-time spacecraft telemetry via CCSDS packets, transmits over UDP, decodes on a ground station, and displays subsystem health in a responsive, minimalist web dashboard.

## 📦 Features

- 🔁 CCSDS-compliant packet encoding/decoding
- 📡 Real-time telemetry transmission (UDP-based)
- 🧠 Subsystem simulation (CDH, POWER, COMMS, ADCS, THERMAL, PROPULSION, PAYLOAD)
- 🧾 CRC validation and sequence tracking
- 🌐 Dynamic mission control dashboard with:
  - Subsystem health indicators
  - Sequence counters
  - Time since last packet
  - Status-responsive pulsing lights
  - Panel routing for detailed subsystem views

---

## 🗂️ Project Structure

```text
project-root/
│
├── src/
│   ├── ccsds/                # Encoder, decoder, APID management
│   ├── subsystems/           # Individual subsystem telemetry simulation
│   ├── static/
│   │   ├── css/              # styles.css
│   │   ├── js/               # main.js
│   │   └── assets/           # logo, icons
│   ├── templates/            # index.html (served by server.py)
│   ├── rx.py                 # Receiver: decodes and relays via WebSocket
│   ├── tx.py                 # Transmitter: encodes and sends packets via UDP
│   └── server.py             # WebSocket + static server
│
├── .env                      # Configuration (IP/PORT)
├── requirements.txt          # Python dependencies
└── README.md
````

---

## 🚀 Getting Started

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/telemetry-dashboard.git
cd telemetry-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure `.env`

```env
GROUND_IP=127.0.0.1
GROUND_PORT=5005
```

### 3. Run the Simulator

In one terminal:

```bash
python src/rx.py     # Receiver/Decoder (Ground Station)
```

In another:

```bash
python src/tx.py     # Transmitter (Spacecraft Simulator)
```

### 4. Launch the Dashboard

In a third terminal:

```bash
python src/server.py
```

Open in browser:
`http://localhost:8000`

---

## 🧪 Tests

Basic encoding/decoding test coverage is provided in the `tests/` directory.
Run with:

```bash
pytest
```

---

## 🧰 Tech Stack

* **Python**: Socket, Struct, psutil
* **Socket.IO**: Real-time server → browser data feed
* **HTML/CSS/JS**: Minimalist static frontend
* **Vanilla JS**: Dynamic grid injection, status logic
* **CCSDS 133.0-B.1**: Packet structure compliance

---

## 📌 TODO Roadmap

* [x] Pulse animation for status lights
* [x] Subsystem routing via panel click
* [ ] Subsystem chart views (D3/Chart.js)
* [ ] Packet logging & historical data
* [ ] Fault simulation injection
* [ ] Subsystem drill-down diagnostics

---

## 📷 Preview

![Mission Control Dashboard](static/assets/dashboard-preview.png)

---

## 🛰️ Author

Developed by Andrew Shields

---

## 📜 License

MIT License – free to use, modify, and launch your own mission.