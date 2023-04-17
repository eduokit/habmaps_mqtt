import requests
import json
import logging
import traceback


class StrapiService:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.host = config['host']
        self.collection = config['collection']
        self.error_file = config['error_file']

    def postData(self, data, collectionId):
        url = f"{self.host}/api/{self.collection[collectionId]}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {"data": data}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                self.logger.error(
                    f"Failed to post data to Strapi. Status code: {response.status_code}. {str(response.reason)}")
                return False
            self.logger.debug(f"Posted data: {str(data)}")
            return True
        except Exception as e:
            self.save_to_file(data)
            print(str(e))
            self.logger.error(
                f'Error sending message: {str(data)}, {str(e)}, {traceback.format_exc()}')
            return False

    def putData(self, data, collectionId,  documentId):
        url = f"{self.host}/api/{self.collection[collectionId]}/{str(documentId)}"
        headers = {"Content-Type": "application/json"}
        payload = {"data": data}
        response = requests.put(url, headers=headers, json=payload)
        try:
            response = requests.put(url, headers=headers, json=payload)
            if response.status_code != 200:
                self.logger.error(
                    f"Failed to PUT data to Strapi. Status code: {response.status_code}. {str(response.reason)}")
                return False
            # self.logger.debug(f"put data: {str(data)}")
            return True
        except Exception as e:
            self.save_to_file(data)
            print(str(e))
            self.logger.error(
                f'Error sending message: {str(data)}, {str(e)}, {traceback.format_exc()}')
            return False

    def getData(self, collectionId):
        url = f"{self.host}/api/{self.collection[collectionId]}"
        response = requests.get(url)

        if response.status_code == 200:
            content = response.json()
            # self.logger.debug(content)
            return content
        else:
            self.logger.error(
                f"La petición GET a Strapi falló con el código de respuesta {response.status_code}")

    def save_to_file(self, data):
        with open(self.error_file, 'a') as f:
            f.write(json.dumps(data) + '\n')
