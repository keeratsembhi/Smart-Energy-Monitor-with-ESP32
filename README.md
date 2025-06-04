# PCB-Based-Smart-Energy-Monitor

A DIY energy monitoring system that measures **real-time voltage, current, and power consumption** using an ESP32, ACS712 current sensor, and ZMPT101B voltage sensor. Readings are logged to a CSV file and optionally visualized or used for threshold-based alerts.

---

## Features

- Measures AC voltage and current using ZMPT101B and ACS712
- Calculates real-time RMS voltage, current, and power (Watts)
- Logs power consumption data into a `.csv` file via Python
- Output can be used for live dashboards, visualizations, or overload detection
- Easily customizable and modular design — add alerts, mobile control, etc.

---
