import json
import websocket
import paho.mqtt.client as mqtt
import time

# MQTT Connection Configuration
broker = "127.0.0.1"
port = 1883
username = ""
password = ""
brokerPrefix = ""

client = mqtt.Client()
client.username_pw_set(username, password)

last_price = None

def format_number(number):
    number_str = str(number)
    decimal_index = number_str.find('.')

    if decimal_index == -1 or len(number_str[:decimal_index]) >= 5:
        return "{:.0f}".format(number)
    else:
        decimal_places = 5 - len(number_str[:decimal_index])
        format_str = "{:." + str(decimal_places) + "f}"
        return format_str.format(number)

def on_connect_mqtt(client, userdata, flags, rc):
    print("Connected to MQTT broker with response code", rc)

def send_via_mqtt(data, app, topic_base=brokerPrefix+"/custom/"):
    message_mqtt = json.dumps(data)
    topic = topic_base + app
    client.publish(topic, message_mqtt)
    print(f"Send {topic}: {message_mqtt}")

def on_message(ws, message):
    global last_price
    data = json.loads(message)
    current_price = float(data['p']) * 100
    price_formatted = format_number(current_price)

    icon = "sc-up" if last_price is not None and current_price > last_price else "sc-down" if last_price is not None and current_price < last_price else "sc"

    data_mqtt_price = {
        "text": price_formatted,
        "icon": icon,
        "pushIcon": 0,
        "repeat": 1,
        "textCase": 1
    }

    send_via_mqtt(data_mqtt_price, "SCUSDT")

    wallet_value = 0
    wallet_formatted = format_number(wallet_value * (current_price / 100))

    data_mqtt_wallet = {
        "text": wallet_formatted,
        "icon": "dollar_sign",
        "pushIcon": 0,
        "repeat": 1,
        "textCase": 1
    }

    send_via_mqtt(data_mqtt_wallet, "MySCWallet")

    last_price = current_price


def connect_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/scusdt@trade",
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open)
            ws.run_forever()
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)



def on_error(ws):
    print("WebSocket connection closed. Trying to reconnect...")

def on_close(ws):
    print("WebSocket connection closed. Trying to reconnect...")
    time.sleep(10)  # Pause for 10 seconds before reconnecting
    connect_websocket()  # Function to reconnect the websocket

def on_open(ws):
    print("Connection opened with WebSocket")

if __name__ == "__main__":
    client.on_connect = on_connect_mqtt
    client.connect(broker, port, 60)
    client.loop_start()
    connect_websocket()

