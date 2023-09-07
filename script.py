import network
import time
import config
import utime
from dht import DHT11
from machine import Pin
from umqtt.simple import MQTTClient
import ujson  

from WifiManager import WifiManager
from MQTTManager import MQTTManager

# Initialize LED (assuming built-in LED is on GPIO 25)

led = Pin("LED", Pin.OUT)
led.on()
# Initialize and connect to WiFi
wifi_manager = WifiManager()
wifi_manager.connect()

# Initialize and connect to MQTT
mqtt_manager = MQTTManager()
client = mqtt_manager.connect()


# Callback function to handle messages
def sub_cb(topic, msg):
    msg = msg.decode('utf-8')
    if msg == "ON":
        led.value(1)
    elif msg == "OFF":
        led.value(0)

# Subscribe to 'led-control' feed
mqtt_manager.subscribe("led-control", sub_cb)


sensor = DHT11(Pin(13))

while True:
    
    try:
        client.check_msg()  # Check for new messages and call the callback function
    except Exception as e:
        print("An exception occurred:", e)
    
    try:
        sensor.measure()
        t = sensor.temperature()
        time.sleep(2)
        h = sensor.humidity()
    except Exception as e:
        print("An exception occurred:", e)
        continue
    
    print("Temperature: {}".format(t))
    print("Humidity: {}".format(h))
    try:
        # Create a JSON object
        data = {
            "temperature": t,
            "humidity": h
        }
        
        # Convert the JSON object to a JSON string
        json_data = ujson.dumps(data)
        
        # Publish the JSON string to Adafruit IO
        mqtt_manager.publish("sensor-data", json_data)
        
    except Exception as e:
        print("An exception occurred during publishing:", e)
    
    # Wait for a second before reading the value again
    #time.sleep(60)