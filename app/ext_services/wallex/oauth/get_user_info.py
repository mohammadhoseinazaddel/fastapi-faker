import json
import requests

from ext_services.wallex.oauth.schemas.wallex_balance_stat import WallexBalanceStat
from system.config import settings
from ext_services.wallex.exceptions.oauth import WallexError
from ext_services.wallex.oauth.schemas.wallex_user_balances import WallexUserBalance
from ext_services.wallex.oauth.schemas.wallex_user_info import WallexUserInfo


def wallex_get_user_info(token: str) -> WallexUserInfo:
    url = settings.WALLEX_API_BASE_UERL + '/v2/oauth/user'

    headers = {
        'Authorization': 'Bearer ' + token
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            response = response.json()

            if 'result' in response and 'id' in response['result']:

                balance_details = []
                user_balances = response['result']['balance_details']
                for item in user_balances.keys():

                    stats = user_balances[item]['stats']
                    balance_stats = []
                    for j in stats.keys():
                        if not stats[j]:
                            continue
                        if 'baseMarketName' not in stats[j]:
                            continue
                        balance_detail = WallexBalanceStat(
                            base_market_name=stats[j]['baseMarketName'],
                            change_percentage=stats[j]['changePercentage'] if 'changePercentage' in stats[j] else None,
                            estimated_value=stats[j]['estimatedValue'] if 'estimatedValue' in stats[j] else None,
                            last_24_hours_estimated_change=stats[j]['last24HoursEstimatedValueChange'] if 'last24HoursEstimatedValueChange' in stats[j] else None,
                        )

                        balance_stats.append(balance_detail)

                    x = WallexUserBalance(
                        symbol=user_balances[item]['symbol'],
                        total=user_balances[item]['total'],
                        freeze=user_balances[item]['freeze'],
                        available=user_balances[item]['available'],
                        stats=balance_stats
                    )
                    balance_details.append(x)

                return WallexUserInfo(
                    wallex_user_id=response['result']['id'],
                    first_name=response['result']['first_name'] if 'first_name' in response['result'] else None,
                    last_name=response['result']['last_name'] if 'last_name' in response['result'] else None,
                    mobile=response['result']['mobile_number'] if 'mobile_number' in response['result'] else None,
                    kyc_level=response['result']['kyc_level'] if 'kyc_level' in response['result'] else None,
                    email=response['result']['email'] if 'email' in response['result'] else None,
                    national_code=response['result']['national_code'] if 'national_code' in response[
                        'result'] else None,
                    birth_date=response['result']['birthday'] if 'birthday' in response['result'] else None,
                    balances_details=balance_details
                )
        else:
            print(response.json())
            raise WallexError
    except Exception as e:
        raise e
