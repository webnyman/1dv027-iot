# mqtt_client.py
from umqtt.simple import MQTTClient

class MQTTClientWrapper:
    def __init__(self, client_id, server, port, user, password):
        self.client = MQTTClient(client_id, server, user=user, password=password, port=port)
        self.client.connect()

    def set_callback(self, callback):
        self.client.set_callback(callback)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, msg):
        self.client.publish(topic, msg)

    def check_msg(self):
        self.client.check_msg()

    def disconnect(self):
        self.client.disconnect()
