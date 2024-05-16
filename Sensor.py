# sensor.py
import time
import dht
import ujson
from machine import Pin

class Sensor:
    def __init__(self, dht_pin=16, led_pin=17):
        self.dht_sensor = dht.DHT22(Pin(dht_pin, Pin.IN, Pin.PULL_UP))
        self.led = Pin(led_pin, Pin.OUT)
        self.led.value(0)  # Ensure LED is off initially

    def read(self):
        try:
            self.dht_sensor.measure()  # Measure the data
            temperature = self.dht_sensor.temperature()  # Get the temperature in Celsius
            humidity = self.dht_sensor.humidity()  # Get the humidity
            self.led.value(1)  # Turn on LED to indicate success
            data = {
                "temperature": temperature,
                "humidity": humidity
            }
            return data  # Return data as a dictionary
        except OSError as e:
            print('Failed to read sensor.')
            self.led.value(0)  # Turn off LED to indicate failure
            return None
