import json
import logging
import traceback
from services.strapi.StrapiService import StrapiService


class StrapiHabmapsService(StrapiService):
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        super().__init__(config)

    def sendToStrapi(self, message):
        self.logger.debug("Se va a preparar el envío a Strapi")
        try:
            messagep = json.loads(message.payload.decode())
            self._sendStrapiMessage(messagep)
        except Exception as e:
            self.logger.error(
                f"Error al parsear el mensaje de entrada. {str(e)}, {traceback.format_exc()}")

    def _sendStrapiMessage(self, messagep):
        '''
        Enviamos el mensaje a una colección de Strapi
        '''
        if messagep['type'] == "frame":
            self.postData({"frame": messagep}, "frame")
            self._postLastSeen(messagep, "frame")
        elif messagep['type'] == "health":
            self.postData({"status": messagep}, "health")
            self._postLastSeen(messagep, "health")
        else:
            self.logger.warning("Message type unknown")

    def _postLastSeen(self, messagep, ftype):
        self.logger.debug("Se va a postear el lastSeen")
        strapiLastSeen = self.getData('lastseen')
        bid = hid = [-404, 0]

        '''
       {'frame': {'type': 'frame', 'ftime': '2023-04-16 20:15:59', 'hab': {'hid': 'HABCAT4', 'pos': {'lat': 9.3074, 'lon': 2.2111}, 'payload': {'AlturaGPS': 1300.0, 'VelocidadHorizontalGPS': 0.9617, 'Temperatura': 102.64, 'Presion': 950.5943, 'AlturaBarometrica': 1083.0, 'BStationHeight': 123.0}}, 'basestation': {'bid': 'id-de-mi-estacion', 'pos': {'lat': 92.3074, 'lon': 62.2111}}}}
        '''
        # 1.- Miramos el tipo de traza y si ya existe registro
        if ftype == 'health':
            bid = self._find_id_by_nameId(strapiLastSeen, messagep['bid'])
            # 2.- Componemos el mensaje
            message = {
                "nameId": messagep['bid'],
                "type": 'basestation',
                "lastSeen": messagep['ftime'],
                "pos": messagep['pos'],
                "counter": 1,
                "payload": {}
            }
            # Updateamos o creamos
            if bid[0] != -404:
                message['counter'] = bid[1] + 1
                self.putData(message, 'lastseen', bid[0])
            else:
                self.postData(message, 'lastseen')

        elif ftype == 'frame':
            bid = self._find_id_by_nameId(
                strapiLastSeen, messagep['basestation']['bid'])
            hid = self._find_id_by_nameId(
                strapiLastSeen, messagep['hab']['hid'])

            # 2.- Componemos el mensaje
            messageBS = {
                "nameId": messagep['basestation']['bid'],
                "type": 'basestation',
                "lastSeen": messagep['ftime'],
                "pos": messagep['basestation']['pos'],
                "counter": 1,
                "payload": {}
            }

            messageHab = {
                "nameId": messagep['hab']['hid'],
                "type": 'hab',
                "lastSeen": messagep['ftime'],
                "pos": messagep['hab']['pos'],
                "counter": 1,
                "payload": messagep['hab']['payload']
            }

            if bid[0] != -404 and hid[0] != -404:
                messageBS['counter'] = bid[1] + 1
                messageHab['counter'] = hid[1] + 1
                self.putData(messageBS, 'lastseen', bid[0])
                self.putData(messageHab, 'lastseen', hid[0])
            else:
                self.postData(messageBS, 'lastseen')
                self.postData(messageHab, 'lastseen')

    def _find_id_by_nameId(self, data, nameId):
        for element in data["data"]:
            if element["attributes"]["nameId"] == nameId:
                return [element["id"], element["attributes"]["counter"]]
        return [-404, 0]
