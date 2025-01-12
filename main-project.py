from hcsr04 import HCSR04
from machine import Pin, PWM
from time import sleep
import simple as mqtt
import network
import time

sensor_e = HCSR04(trigger_pin=18, echo_pin=19, echo_timeout_us=10000)
sensor_w = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=10000)

servo = PWM(Pin(16))
servo.freq(50)

SSID = 'AndroidAP0c21'
PASSWORD = 'ilrc2120'

mqtt_server = '192.168.43.202'
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
    if msg.decode() == "1":
        set_servo_angle(0)
        message = "Bariera inchisa"
    else:
        set_servo_angle(90)
        message = "Bariera deschisa"
    print(message)

def set_servo_angle(angle):
    duty = int((angle / 180 * 4915) + 1638)
    servo.duty_u16(duty)


connect_wifi()

try:
    client.set_callback(on_message)
    client.connect()
    print("Conectat la broker MQTT")
    client.subscribe("test/barrier")

    while True:
        distance_e = sensor_e.distance_cm()
        distance_w = sensor_w.distance_cm()
        message = f"E-{abs(distance_e)},W-{abs(distance_w)}"
        client.publish(topic, message)

        client.check_msg()
        sleep(1)
 
except Exception as e:
    print("Eroare de conectare:", e)
finally:
    client.disconnect()
    print("Deconectat de la broker MQTT")