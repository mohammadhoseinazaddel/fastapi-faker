import json
import requests
from system.config import settings
from ext_services.wallex.exceptions.oauth import WallexError


def wallex_get_oauth_url(state: str):
    url = settings.WALLEX_API_BASE_UERL + '/v2/oauth/authorize-url'

    params = {
        'response_type': 'code',
        'client_id': settings.WALLEX_LOGIN_CLIENT_ID,
        'redirect_uri': settings.CALLBACK_URL_FROM_WALLEX_LOGIN,
        'scope': 'user-info',
        'state': state  # CSRF token
    }

    try:
        response = requests.get(url, params=params, verify=False)
        if response.status_code == 200:
            res = json.loads(response.text)
            if 'result' in res and 'url' in res['result']:
                return res['result']['url']
            return res
        else:
            print(response.json())
            raise WallexError

    except Exception as e:
        raise e


