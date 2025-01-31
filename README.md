# IoT Health Surveillance System

## 📌 Overview
IoT-based real-time health monitoring system using ESP32, MQTT, and Raspberry Pi as a broker. Node-RED processes and displays SpO2, heart rate, and temperature data, storing it in Firebase for trend analysis and anomaly detection. A React interface provides dynamic visualizations.

## 📁 Project Structure
- `/arduino_code/` - Arduino scripts for data collection.
- `/python_scripts/` - Python scripts for data processing and analytics.
- `flowchart.json` - Flowchart representation of the system.
- `/patient-visualization/` - React frontend.

## ⚡ Features
- Real-time health data monitoring
- Alerts and notifications for anomalies


## 🚀 Installation
### Requirements for python code
```bash
pip install 

## 🚀 Running the React Interface
Navigate to the frontend directory:
```sh
cd patient-visualization
npm install
npm run dev