from paho.mqtt.client import Client
from elasticsearch import Elasticsearch
import datetime
import pytz

bucharest_tz = pytz.timezone("Europe/Bucharest")

manual_mode = False
manual_command = "0"

es = Elasticsearch("https://localhost:9200",
                   basic_auth=("elastic", "hoG9ZsOilolQQiGMxKX2"),
                   verify_certs=True,
                   ca_certs="certs/ca.crt")

def on_message(client, userdata, msg):
    global manual_mode, manual_command

    if msg.topic == "test/mode":
        print(f"Mode change request received: {msg.payload.decode()}")
        manual_mode = (msg.payload.decode() == "manual")
        print(f"Mode changed to {'manual' if manual_mode else 'auto'}")
        return
    
    if manual_mode and msg.topic == "test/manual":
        manual_command = msg.payload.decode()
        print(f"Manual command received: {manual_command}")
        client.publish("test/barrier", manual_command)
        return

    if not manual_mode and msg.topic == "test/parking-data":
        occupied_slots = {}
        sensors = msg.payload.decode().split(",")

        for sensor in sensors:
            sensor_id, distance = sensor.split("-")
            distance = float(distance)
            occupied_slots[sensor_id] = distance < 10

        data = {}
        data["sensors"] = occupied_slots.copy()
        data["timestamp"] = datetime.datetime.now(bucharest_tz).isoformat()
        es.index(index="parking_data", body=data)

        parking_full = all(data["sensors"].values())
        client.publish("test/barrier", "1" if parking_full else "0")


mqtt_client = Client()
mqtt_client.connect("127.0.0.1")
mqtt_client.subscribe("test/parking-data")
mqtt_client.subscribe("test/mode")
mqtt_client.subscribe("test/manual")
mqtt_client.on_message = on_message
mqtt_client.loop_forever()
