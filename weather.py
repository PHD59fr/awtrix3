import json
from unidecode import unidecode
import requests
import paho.mqtt.client as mqtt

# MQTT Connection Configuration
broker = "127.0.0.1"
port = 1883
username = ""
password = ""
brokerPrefix = ""

client = mqtt.Client()
client.username_pw_set(username, password)

# OpenWeatherMap API Configuration
api_key = "APIKEY"
latitude = "48.8907"
longitude = "2.2420"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=fr"

# Updated dictionary to map French weather descriptions to Awtrix icons
weather_icons = {
    "averses de neige": "w-snowy-rainy",
    "brouillard": "w-fog",
    "bruine légère": "w-fog",
    "brume légère": "w-fog",
    "brume": "w-fog",
    "ciel dégagé": "w-sunny",
    "couvert": "w-cloudy",
    "forte pluie": "w-pouring",
    "grêle": "w-hail"
    "légère pluie": "w-rainy",
    "neige légère": "w-snowy",
    "neige": "w-snowy",
    "nuageux": "w-cloudy",
    "orage et pluie fine": "w-lightning",
    "orage et pluie": "w-lightning",
    "orage": "w-lightning",
    "partiellement nuageux": "w-partlycloudy",
    "peu nuageux": "w-partlycloudy",
    "pluie et neige": "w-snowy-rainy",
    "pluie extreme": "w-pouring",
    "pluie modérée": "w-rainy",
    "pluie très fine": "w-rainy",
    "très forte pluie": "w-pouring",
}

def on_connect_mqtt(client, userdata, flags, rc):
    print("Connected to MQTT broker with response code", rc)

def send_via_mqtt(data, app, topic_base=brokerPrefix+"/custom/"):
    message_mqtt = json.dumps(data)
    topic = topic_base + app
    client.publish(topic, message_mqtt)
    print(f"Sent {topic}: {message_mqtt}")

def fetch_and_send_weather_data():
    response = requests.get(url)
    weather_data = response.json()

    if weather_data:
        temp = weather_data["main"]["temp"]
        weather_main = weather_data["weather"][0]["main"].lower()  # Use "main" for a broader match
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        icon_key = description.lower()  # Key for the dictionary
        icon = weather_icons.get(icon_key, "w-exceptional")  # Use 'w-exceptional' as default icon

        data_mqtt_weather = {
            "text": f"{unidecode(description.capitalize())}, T: {temp}°C - H: {humidity}% - V: {wind_speed} km/h",
            "icon": icon,
            "pushIcon": 0,
            "repeat": 2,
            "textCase": 1
        }

        send_via_mqtt(data_mqtt_weather, "Weather")

if __name__ == "__main__":
    client.on_connect = on_connect_mqtt
    client.connect(broker, port, 60)
    client.loop_start()

    # Fetch and send weather data
    fetch_and_send_weather_data()

