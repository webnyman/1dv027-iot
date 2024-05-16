import config
from WifiManager import WifiManager
from Sensor import Sensor
from MQTTManager import MQTTClientWrapper
import time
import ujson
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
    wifi_manager = WifiManager(config.WIFI_SSID, config.WIFI_PASSWORD)
    sensor = Sensor()

    topic = "{}/feeds/led-control".format(config.AIO_USERNAME)

    mqtt_client = MQTTClientWrapper(
        client_id="pico",
        server="io.adafruit.com",
        port=1883,
        user=config.AIO_USERNAME,
        password=config.AIO_KEY
    )

    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.subscribe(topic)

    try:
        wifi_manager.connect()
        wifi_manager.led.value(1)

        sensor_topic = "{}/feeds/temperature".format(config.AIO_USERNAME)

        global led
        led = Pin("LED", Pin.OUT)  # Initialize the built-in LED pin

        while True:
            sensor_data = sensor.read()
            if sensor_data:
                # Convert the dictionary to a JSON string and then to bytes
                sensor_data_json = ujson.dumps(sensor_data)
                sensor_data_bytes = sensor_data_json.encode("utf-8")
                print("Publishing to MQTT: {}".format(sensor_data_json))
                mqtt_client.publish(sensor_topic, sensor_data_bytes)
            else:
                print("Failed to read from the sensor")

            mqtt_client.check_msg()

            time.sleep(5)

    except RuntimeError as e:
        print(e)
        while True:
            wifi_manager.blink_led()


if __name__ == "__main__":
    main()
