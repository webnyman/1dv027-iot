import time
import dht
from machine import Pin

# Define the sensor
dht_pin = Pin(16, Pin.IN, Pin.PULL_UP)  # Data pin connected to GP16
sensor = dht.DHT22(dht_pin)

def read_sensor():
    try:
        sensor.measure()  # Measure the data
        temperature = sensor.temperature()  # Get the temperature in Celsius
        humidity = sensor.humidity()  # Get the humidity
        return temperature, humidity
    except OSError as e:
        print('Failed to read sensor.')
        return None, None

# Main loop
while True:
    temp, hum = read_sensor()
    if temp is not None and hum is not None:
        print('Temperature: {:.1f} C'.format(temp))
        print('Humidity: {:.1f} %'.format(hum))
    else:
        print('Failed to read from the sensor')
    time.sleep(2)  # Wait for 2 seconds before reading again
