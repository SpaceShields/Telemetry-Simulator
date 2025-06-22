# TLI Telemetry Simulator 🛰️

TLI Telemetry Simulator is a Python-based simulation of unencrypted spacecraft telemetry modeled on CCSDS standards. Designed for real-time streaming from a Raspberry Pi 5 (acting as the spacecraft) to a ground station (your home PC), this project replicates the downlink of telemetry packets during a simulated Trans-Lunar Injection (TLI) burn.
🔧 Features

    CSV-based subsystem data (battery, GNC) as time-series input

    CCSDS-compliant packet construction with optional framing (ASM, headers)

    UDP-based transmission to a ground station receiver

    Modular architecture for encoding, streaming, decoding, and visualization

    Designed for extensibility with real-world packet structures and virtual channel multiplexing

🚀 Technologies

    Python 3

    Socket networking (UDP)

    CSV parsing & packet encoding

    CCSDS protocol modeling

    Optional: matplotlib, struct, dataclasses