import common.log
from configuration.MqttConfig import MqttConfig
from services.mqtt.MqttService import MqttService
from configuration.StrapiConfig import StrapiConfig
from services.habmaps.StrapiHabmapsService import StrapiHabmapsService
import os
import logging


class Connector(MqttService):
    def __init__(self, config):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)
        self.topic = config['topic']
        self.subscribe(config['topic'])

        # Cargamos la lógica de lo que se hará una vez llegue un
        # mensaje.
        self.strapiHabmapsService = StrapiHabmapsService(
            StrapiConfig(os.getenv('CONFIG_FILE')).getConfig())

    def on_message(self, client, userdata, message):
        self.logger.debug(
            f'Received message on topic {message.topic}')
        self.strapiHabmapsService.sendToStrapi(message)


connector = Connector(MqttConfig(os.getenv('CONFIG_FILE')).getConfig())
connector.run()
