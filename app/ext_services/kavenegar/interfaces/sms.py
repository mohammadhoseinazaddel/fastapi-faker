import aiohttp
import requests

from system.config import settings


class KavenegarInterface:
    def __init__(self, kavenegar_api_key):
        self.kavenegar_api_key = kavenegar_api_key

    async def send_sms(
            self,
            receptor: str,
            message: str,
            line_number: str,
            local_message_id: int,
            provider_id: int
    ):

        """
            Create this method as coroutine because we have I/O waiting, and we should process them concurrently.
            Using "aiohttp" instad of "requests" library to handle async requests
        """
        try:

            request_url = f'https://api.kavenegar.com/v1/{self.kavenegar_api_key}/sms/send.json'
            async with aiohttp.ClientSession() as session:
                async with session.post(url=request_url, data={"receptor": receptor, 'message': message,
                                                               'sender': line_number}) as response:
                    response = await response.json()
                    if response['return']['status'] == 418:
                        raise SystemError("The balance of account is not enough")
                    return response, local_message_id, provider_id

        except Exception as e:
            raise e

    def check_status(self, message_ids: list):
        try:
            if len(message_ids) > 500:
                raise ValueError("message ids count should be less than or equal 500")

            """
             after json.loads(response.content.decode('UTF8'))['entries']
             we got:
                [
                    {'messageid': 1405363848,
                     'status': 10,
                      'statustext': 'رسیده به گیرنده'
                    },
                    {'messageid': 1405363849,
                     'status': 10,
                      'statustext': 'رسیده به گیرنده'
                      }
                ]
            :param message_ids:
            :return:
            """
            message_ids_in_str_format = ','.join(map(str, message_ids))
            url = f'https://api.kavenegar.com/v1/{self.kavenegar_api_key}/sms/status.json?messageid={message_ids_in_str_format}'
            response = requests.get(url=url)
            return response
        except Exception as e:
            raise e

    @staticmethod
    def map_kavenegar_status_code_to_our_statuses(code: int):
        from notification.notification_service import NotificationService

        """
            Map kavenegar status codes to our statemachine status codes
        """
        notification_sr = NotificationService()

        if code in [1, 2]:
            return notification_sr.sms.crud.STATUS_SENDING

        if code in [4, 5, 10, 11, 13, 14]:
            return notification_sr.sms.crud.STATUS_SENT

        if code in [6]:
            return notification_sr.sms.crud.STATUS_FAILED


kavenegar_agent = KavenegarInterface(settings.KAVENEGAR_API_KEY)
