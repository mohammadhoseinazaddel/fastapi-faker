import requests


class WallexPriceInterface():
    def __init__(self):
        self.api_address = 'https://api.wallex.ir/v1/otc/markets'

    def get_otc_price_list(self):
        try:
            response = requests.get(self.api_address)
        except Exception as e:
            raise e

        if response.status_code == 200:
            return response.json()

        else:
            print(response.json())
