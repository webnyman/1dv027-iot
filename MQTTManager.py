
from umqtt.simple import MQTTClient
import config

class MQTTManager:
    def __init__(self):
        self.client_id = config.CLINET_ID
        self.client = MQTTClient(self.client_id, "io.adafruit.com", 
                                 user=config.ADAFRUIT_IO_USERNAME, 
                                 password=config.ADAFRUIT_IO_KEY, port=1883)
        
    def connect(self):
        self.client.connect()
        return self.client

    # Make it possible to publish data to two different feeds
    def publish(self, feed, data):
        topic = "{}/feeds/{}".format(config.ADAFRUIT_IO_USERNAME, feed)
        self.client.publish(topic, str(data))
        
    # Set Pico on On or OFF
    def subscribe(self, feed, callback):
        topic = "{}/feeds/{}".format(config.ADAFRUIT_IO_USERNAME, feed)
        self.client.set_callback(callback)
        self.client.subscribe(topic)
