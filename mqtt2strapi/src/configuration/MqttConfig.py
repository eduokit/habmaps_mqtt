import yaml
import logging


class MqttConfig:
    def __init__(self, config_path):
        self.logger = logging.getLogger(__name__)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['mqtt']

    def getConfig(self):
        if not self.validate():
            raise Exception('MQTT configuration validation failed')

        return self.config

    def validate(self):
        self.logger.info('Validating MQTT configuration')
        errors = []

        if 'topic' not in self.config:
            errors.append('Missing MQTT topic configuration')
        if 'host' not in self.config:
            errors.append('Missing MQTT host configuration')
        if 'port' not in self.config:
            errors.append('Missing MQTT port configuration')
        if 'user' not in self.config:
            errors.append('Missing MQTT user configuration')
        if 'password' not in self.config:
            errors.append('Missing MQTT password configuration')

        if errors:
            self.logger.error(
                'MQTT configuration validation failed: %s', ', '.join(errors))
            return False
        else:
            self.logger.info('MQTT configuration validation successful')
            return True
