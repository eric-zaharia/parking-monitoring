from paho.mqtt.client import Client
from elasticsearch import Elasticsearch
import datetime

es = Elasticsearch("https://localhost:9200", 
                   verify_certs=False,
                   http_auth=("elastic", "J1EWyeues0mlR=ws374N"))


def on_message(client, userdata, msg):
    occupied_slots = {}
    sensors = msg.payload.decode().split(",")

    for sensor in sensors:
        sensor_id, distance = sensor.split("-")
        distance = float(distance)
        occupied_slots[sensor_id] = distance < 10

    data = {}
    data["sensors"] = occupied_slots.copy()
    data["timestamp"] = datetime.datetime.now().isoformat()
    es.index(index="parking_data", body=data)

    parking_full = all(data["sensors"].values())
    client.publish("test/barrier", "1" if parking_full else "0")

mqtt_client = Client()
mqtt_client.connect("127.0.0.1")
mqtt_client.subscribe("test/parking-data")
mqtt_client.on_message = on_message
mqtt_client.loop_forever()
