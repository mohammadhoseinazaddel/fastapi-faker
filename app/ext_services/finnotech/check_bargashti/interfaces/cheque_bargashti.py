import requests
from sqlalchemy.orm import Session

from ext_services.finnotech.check_bargashti.exceptions.cheque_bargashti import FinnotechChequeBargashtiError, \
    FinnotechChequeCompabilityError
from system.base.mixins import InterfaceLifeCycle
from system.config import settings


class FinotechChequeBargashti(InterfaceLifeCycle):

    def __init__(self):
        self.transactions = None

    def cheque_bargashti(self, db: Session, national_code: str, track_id: str = None):

        url = settings.FINNOTECH_BASE_URL + f'/credit/v2/clients/{settings.FINNOTECH_CLIENT_ID}/users/{national_code}/backCheques'
        if track_id:
            url += '?trackId=' + track_id

        headers = {
            "Authorization": "Bearer " + settings.FINNOTECH_ACCESS_TOKEN
        }

        result = requests.get(url=url, headers=headers, verify=False)

        res = {
            'national_code': national_code,
            'has_cheque_bargashti': None,
            'track_id': None,
        }

        if result.status_code == 200:
            result = result.json()

            if 'trackId' in result:
                res['track_id'] = result['trackId']

            if 'result' in result:
                if 'chequeList' in result['result'] and result['result']['chequeList']:
                    res['has_cheque_bargashti'] = True

                elif 'result' in result['result']:
                    if result['result']['result'] == 110:
                        res['has_cheque_bargashti'] = False

            else:
                raise FinnotechChequeCompabilityError

            return res

        else:
            result = result.json()
            # res['status'] = 'FAILED'

            if 'status' in result and result['status'] == 'FAILED':
                if 'error' in res:
                    code = result['error']['code'] if 'code' in result['error'] else None
                    message = result['error']['message'] if 'message' in result['error'] else None

                    raise FinnotechChequeBargashtiError(message=message, error_code=code)

            raise FinnotechChequeBargashtiError


finnotech_cheque_bargashti_agent = FinotechChequeBargashti()
