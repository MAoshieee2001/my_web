import time

import requests


class ApiConsume:

    def __init__(self):
        self.base_url = 'https://apiperu.dev/api/dni/'
        self.token = '102c6b44c1919a2549ced592807f1475b526d84f3ac8a23e3608754863e11c29'

    def get_customer_dni(self, dni):
        data = {}
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        payload = {
            'dni': dni
        }
        try:
            start_time = time.time()
            r = requests.post(self.base_url, headers=headers, data=payload)
            if r.status_code == 200:
                data = r.text
            else:
                data['error'] = r.json()
            end_time = time.time()
            latency = end_time - start_time
            print(latency)
        except Exception as e:
            data['error'] = str(e)
        return data