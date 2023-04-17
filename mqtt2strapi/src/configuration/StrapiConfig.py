import yaml
import logging


class StrapiConfig:
    def __init__(self, config_path):
        self.logger = logging.getLogger(__name__)
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['strapi']

    def getConfig(self):
        if not self.validate():
            raise Exception('Strapi configuration validation failed')

        return self.config

    def validate(self):
        self.logger.info('Validating Strapi configuration')
        errors = []

        if 'host' not in self.config:
            errors.append('Missing Strapi host configuration')
        if 'user' not in self.config:
            errors.append('Missing Strapi user configuration')
        if 'password' not in self.config:
            errors.append('Missing Strapi password configuration')
        if 'collection' not in self.config:
            errors.append('Missing Strapi collection configuration')

        if errors:
            self.logger.error(
                'Strapi configuration validation failed: %s', ', '.join(errors))
            return False
        else:
            self.logger.info('Strapi configuration validation successful')
            return True
