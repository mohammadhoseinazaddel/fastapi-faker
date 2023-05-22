import requests

from system.config import settings


class SmsIrInterface():
    def __init__(self):
        self.something = ''

    def get_token(self):
        url = settings.SMS_IR_BASE_URL + '/api/Token'

        header = {
            "Content-Type": "application/json"
        }

        json_body = {
            "UserApiKey": settings.SMS_IR_SECRET_KEY,
            "SecretKey": settings.SMS_IR_API_KEY
        }

        res = requests.post(url=url, json=json_body,headers=header, verify=False)

        if res.status_code == 201:
            res = res.json()

            if "TokenKey" in res and res["TokenKey"]:
                settings.SMS_IR_TOKEN = res["TokenKey"]

        else:
            pass

        return res

    # def send_sms(self, db: Session, mobiles: List[str], messages: List[str]):
    #     url = settings.SMS_IR_BASE_URL + '/api/MessageSend'
    #
    #     header = {
    #         "Content-Type": "application/json",
    #         "x-sms-ir-secure-token": settings.SMS_IR_TOKEN
    #     }
    #
    #     json_body = {
    #         "Messages": messages,
    #         "MobileNumbers": mobiles,
    #         "LineNumber": settings.SMS_IR_LINE_NUMBER,
    #         "SendDateTime": None,
    #         "CanContinueInCaseOfError": True,
    #     }
    #
    #     res = requests.post(url=url, json=json_body, headers=header, verify=False)
    #
    #     return res.json()

    @staticmethod
    def send_otp_khadamati(mobile: str, otp: str):
        url = settings.SMS_IR_BASE_URL + '/api/UltraFastSend/direct'

        header = {
            "Content-Type": "application/json",
        }

        json_body = {
            "ParameterArray": [{
                "Parameter": "otp",
                "ParameterValue": otp,
            }],
            "Mobile": mobile,
            "TemplateId": "72733",
            "UserApiKey": settings.SMS_IR_SECRET_KEY,
            "SecretKey": settings.SMS_IR_API_KEY,

        }

        res = requests.post(url=url, json=json_body, headers=header, verify=False)

        return res.json()


sms_ir_agent = SmsIrInterface()
