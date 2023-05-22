from sqlalchemy.orm import Session
import requests
import base64
from system.base.mixins import InterfaceLifeCycle
from system.config import settings


class FinotechTokenInterface(InterfaceLifeCycle):

    def __init__(self):
        self.transactions = None

    def get_token(self, db: Session):
        url = settings.FINNOTECH_BASE_URL + '/dev/v2/oauth2/token'

        txt_to_encode = settings.FINNOTECH_CLIENT_ID + ":" + settings.FINNOTECH_CLIENT_SECRET
        b = base64.b64encode(bytes(txt_to_encode, 'utf-8'))
        base64_str = b.decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64_str
        }

        json_body = {
            "grant_type": "client_credentials",
            "nid": '1142332209',
            "scopes": settings.FINNOTECH_SCOPES
        }

        res = requests.post(url=url, headers=headers, json=json_body, verify=False)

        if res.status_code == 200:
            res = res.json()
            settings.FINNOTECH_ACCESS_TOKEN = res['result']['value']
            settings.FINNOTECH_REFRESH_TOKEN = res['result']['refreshToken']

        return res


finnotech_token_agent = FinotechTokenInterface()
