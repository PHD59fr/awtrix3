# 🖥️ Scripts for AWTRIX

## 📝 Description

This Python project publishes a message to an MQTT broker, displaying a percentage that represents the progress of the current year. The percentage is calculated based on the time elapsed since the beginning of the year and is sent as a JSON message to an MQTT-compatible device or application, such as an Awtrix display.

## 📋 Prerequisites

- 🐍 Python 3.x
- 📦 `paho-mqtt` library
- 🖧  mqtt server (ex: mosquitto)

To install `paho-mqtt`, run the following command:

```bash
pip install paho-mqtt
```

## ⚙️ Configuration

Before running the script, configure the following parameters:

- **🌐 broker**: The IP address or domain name of your MQTT broker.
- **🔌 port**: The port used by the MQTT broker.
- **👤 username**: The username to connect to the MQTT broker.
- **🔑 password**: The password to connect to the MQTT broker.
- **📡 topic**: The MQTT topic where the message will be published.

Don't forget to upload the necessary icons for display on the Awtrix.

## 🛠️ How It Works

### 🧩 JSON Message Creation

Once the progress is calculated, it is formatted into a JSON message that includes the percentage, an icon representing the year, and other display parameters.

Example JSON message:

```json
{
    "text": "67%",
    "icon": "2024",
    "pushIcon": 0,
    "repeat": 1,
    "textCase": 2
}
```

### 🚀 MQTT Message Publishing

The script then connects to the MQTT broker using the provided credentials. Once connected, the message is published to the specified topic. After publishing, the MQTT client disconnects cleanly from the broker.

## ▶️ Execution

To run the script, ensure your MQTT broker is running and accessible, then execute the script with Python:

```bash
python script_mqtt.py
```

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute it under the terms of the license.
