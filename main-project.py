from hcsr04 import HCSR04
from time import sleep
import simple as mqtt
import network
import time

sensor_ne = HCSR04(trigger_pin=18, echo_pin=19, echo_timeout_us=10000)
sensor_se = HCSR04(trigger_pin=20, echo_pin=21, echo_timeout_us=10000)
sensor_nw = HCSR04(trigger_pin=10, echo_pin=11, echo_timeout_us=10000)
sensor_sw = HCSR04(trigger_pin=12, echo_pin=13, echo_timeout_us=10000)

SSID = 'Eric\'s iPhone'
PASSWORD = 'parolaeric'

mqtt_server = '172.20.10.3'
client_id = 'pico'
topic = 'test/parking-data'

client = mqtt.MQTTClient(client_id, mqtt_server, port=1883)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Conectare la Wi-Fi...")
        time.sleep(1)
    print("Conectat la Wi-Fi:", wlan.ifconfig())

def on_message(topic, msg):
    message = "Bariera inchisa" if msg.decode() == "1" else "Bariera deschisa"
    print(message)


connect_wifi()

try:
    client.set_callback(on_message)
    client.connect()
    print("Conectat la broker MQTT")
    client.subscribe("test/barrier")

    while True:
        distance = sensor_ne.distance_cm()
        message = f"NE-{distance},SE-5,NW-5,SW-5"
        client.publish(topic, message)

        client.check_msg()
        sleep(1)
 
except Exception as e:
    print("Eroare de conectare:", e)
finally:
    client.disconnect()
    print("Deconectat de la broker MQTT")