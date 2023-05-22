import json
import requests
from system.config import settings
from ext_services.wallex.exceptions.oauth import WallexError


def wallex_get_token_by_code(code: str):
    url = settings.WALLEX_API_BASE_UERL + '/v2/oauth/token'

    var = {
        'grant_type': 'authorization_code',  # 'authorization_code', 'client_credential'
        'client_id': settings.WALLEX_LOGIN_CLIENT_ID,
        'client_secret': settings.WALLEX_LOGIN_CLIENT_SECRET,
        'redirect_uri': settings.CALLBACK_URL_FROM_WALLEX_LOGIN,
        # 'redirect_uri': 'https://api.stage.wallpay.org/api/v1/user/login/wallex-callback',
        'code': code  # CSRF token
    }

    try:
        response = requests.post(url, json=var, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.json())
            raise WallexError

    except Exception as e:
        raise e

