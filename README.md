# **Smart Parking Monitoring System**

This repository contains the code and instructions for setting up a smart parking monitoring system. The system uses ultrasonic sensors to detect parking slot occupancy and an MQTT protocol to transmit data to Elasticsearch for real-time visualization in Kibana.

---

## **Features**
- Measures parking slot occupancy using HCSR04 ultrasonic sensors.
- Publishes sensor data to an MQTT broker.
- Sends data to Elasticsearch for storage and analysis.
- Visualizes data in Kibana dashboards.
- Automates barrier control with a servo motor (optional).

---

## **Prerequisites**
### **Hardware**
- Raspberry Pi Pico WH (with MicroPython firmware)
- HCSR04 Ultrasonic Sensors (4x)
- Servo Motor (optional for barrier control)
- Wi-Fi network for communication

### **Software**
- Python 3.10+ on your PC
- MicroPython environment set up on Raspberry Pi Pico WH
- MQTT Broker (e.g., Mosquitto)
- Elasticsearch and Kibana installed locally or on a server

---

## **Setup and Usage**

### **1. Hardware Connections**
- Connect each HCSR04 ultrasonic sensor to the GPIO pins on the Raspberry Pi Pico WH:
  - Sensor NE: Trigger pin 18, Echo pin 19
  - Sensor SE: Trigger pin 20, Echo pin 21
  - Sensor NW: Trigger pin 10, Echo pin 11
  - Sensor SW: Trigger pin 12, Echo pin 13
- (Optional) Connect the servo motor to a GPIO pin on the Raspberry Pi Pico WH.

### **2. Software Installation**

### Install Python Libraries
1. On your local machine, install the required Python libraries:
   \`\`\`
   pip install paho-mqtt elasticsearch
   \`\`\`

### Setup MicroPython on Raspberry Pi Pico WH
1. **Install Thonny IDE** (or use any compatible tool) and flash MicroPython firmware onto the Raspberry Pi Pico WH.
2. Download the latest MicroPython firmware from the official [MicroPython website](https://micropython.org/download).
3. Follow the flashing instructions provided by the MicroPython documentation to load the firmware onto your device.

### Connect to Wi-Fi
1. **Open the MicroPython script** on your Raspberry Pi Pico WH (`main-project.py`)**.
3. Set the Wi-Fi credentials:
   \`\`\`
   SSID = 'Your-WiFi-SSID'
   PASSWORD = 'Your-WiFi-Password'
   \`\`\`
4. Connect the Raspberry Pi Pico WH to your Wi-Fi network:
   \`\`\`
   import network
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)
   wlan.connect(SSID, PASSWORD)
   while not wlan.isconnected():
       print("Connecting to Wi-Fi...")
       time.sleep(1)
   print("Connected to Wi-Fi:", wlan.ifconfig())
   \`\`\`

### Configure MQTT
1. **Update the MQTT broker IP address** in the MicroPython script:
   \`\`\`
   mqtt_server = 'Your-MQTT-Broker-IP'
   \`\`\`
2. Upload the script to the Raspberry Pi Pico WH and run it:
   \`\`\`
   python pico_sensor_data.py
   \`\`\`

### Configure and Run Data Processing Script
1. **Open the Python script for processing and forwarding data (`es_proxy.py`)** on your local machine.
2. **Update the Elasticsearch connection settings**:
   \`\`\`
   es = Elasticsearch("http://localhost:9200", http_auth=("elastic", "your-password"))
   \`\`\`
3. **Update the MQTT broker IP address**:
   \`\`\`
   mqtt_client.connect("Your-MQTT-Broker-IP")
   \`\`\`
4. **Run the script**:
   \`\`\`
   python es_proxy.py
   \`\`\`

### Set Up Elasticsearch and Kibana
1. **Start Elasticsearch**:
   \`\`\`
   ./bin/elasticsearch
   \`\`\`
2. **Start Kibana**:
   \`\`\`
   ./bin/kibana
   \`\`\`
3. **Create an index pattern in Kibana** (e.g., `parking_data*`).
4. **Build visualizations** (e.g., time-series charts) to monitor parking data.
\`\`\`
