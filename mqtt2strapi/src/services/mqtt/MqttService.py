import paho.mqtt.client as mqtt
import logging
import time


class MqttService():
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.client = None
        self.client = mqtt.Client()
        self.client.username_pw_set(
            self.config['user'], password=self.config['password'])
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def connect(self):
        self.client.connect(self.config['host'], int(self.config['port']))

    def on_connect(self, client, userdata, flags, rc):
        self.logger.debug('MQTT client connected with result code %s', rc)
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, message):
        self.logger.debug('MQTT message received on topic %s', message.topic)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.error(
                'Disconnected from MQTT broker with error code %s. Trying to reconnect...', rc)
            self.client.reconnect()

    def run(self):
        self.connect()
        self.client.loop_forever()

    def publish(self, topic, payload):
        try:
            self.client.publish(topic, payload)
        except Exception:
            self.logger.exception(
                'MQTT publish failed, trying to reconnect...')

    def subscribe(self, topic):
        self.topic = topic
