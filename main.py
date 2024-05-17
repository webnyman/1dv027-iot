import config
from WifiManager import WifiManager
from Sensor import Sensor
from MQTTManager import MQTTClientWrapper
import time
import ujson
import gc
from machine import Pin

# Callback function to handle messages
def mqtt_callback(topic, msg):
    message = msg.decode("utf-8")
    print("Received message: {} on topic: {}".format(message, topic))
    if message == "ON":
        led.value(1)
    elif message == "OFF":
        led.value(0)

def main():
    gc.collect()  # Run garbage collection to free up memory

    # Initialize WiFi manager and connect to WiFi
    wifi_manager = WifiManager(config.WIFI_SSID, config.WIFI_PASSWORD)
    try:
        wifi_manager.connect()
    except RuntimeError as e:
        print("WiFi connection failed:", e)
        return

    # WiFi is connected, set the WiFi LED to on
    wifi_manager.led.value(1)
    print("Network config:", wifi_manager.wlan.ifconfig())

    # Delay to ensure WiFi connection is stable
    time.sleep(5)

    # Initialize the MQTT client
    mqtt_client = MQTTClientWrapper(
        client_id="pico",
        server="io.adafruit.com",
        port=1883,
        user=config.AIO_USERNAME,
        password=config.AIO_KEY
    )

    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.subscribe("{}/feeds/led-control".format(config.AIO_USERNAME))

    global led
    led = Pin("LED", Pin.OUT)  # Initialize the built-in LED pin
    green_led = Pin(12, Pin.OUT)  # Initialize the green LED pin

    # Set up a timer to control the sensor data publishing interval
    last_publish_time = time.time()
    publish_interval = 5  # Time interval in seconds

    sensor = Sensor()  # Initialize the sensor after setting up WiFi and MQTT

    try:
        while True:
            current_time = time.time()

            # Check if it's time to publish sensor data
            if current_time - last_publish_time >= publish_interval:
                sensor_data = sensor.read()
                if sensor_data:
                    temperature = sensor_data["temperature"]
                    humidity = sensor_data["humidity"]

                    # Publish temperature and humidity to their respective feeds
                    print(f'Publishing temperature: {temperature}')
                    mqtt_client.publish("{}/feeds/temperature".format(config.AIO_USERNAME), str(temperature))
                    
                    print(f'Publishing humidity: {humidity}')
                    mqtt_client.publish("{}/feeds/humidity".format(config.AIO_USERNAME), str(humidity))
                    
                    last_publish_time = current_time
                    green_led.value(1)  # Turn on green LED to indicate success
                else:
                    print("Failed to read from the sensor")
                    green_led.value(0)  # Turn off green LED to indicate failure

            # Check for incoming messages
            mqtt_client.check_msg()
                
            time.sleep(0.1)  # Short sleep to prevent 100% CPU usage

    except Exception as e:
        print("Exception:", e)
        while True:
            wifi_manager.blink_led()  # Indicate error state by blinking WiFi LED

if __name__ == "__main__":
    main()
