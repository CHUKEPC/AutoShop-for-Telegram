import time
import random
import secrets
import aiohttp
from tgbot.data import config

class Lolz:
    def __init__(self, access_token: str):
        self.api_url = 'https://api.zelenka.guru/'
        self.session_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        self.timeout = aiohttp.ClientTimeout(total=360)

    async def get_user(self):
        async with aiohttp.ClientSession(headers=self.session_headers, timeout=self.timeout) as session:
            response = await session.get('https://api.lzt.market/me', timeout=self.timeout)
            if response.status == 200:
                response = await response.json()
                await session.close()
                if 'user' not in response.keys():
                    raise ValueError('Invalid Token [Lolzteam Market]')
                return response['user']
            else:
                error = await response.text()
                await session.close()
                error = error.split('<h1>')[1].split('</h1>')[0]
                raise BaseException(error)

    def get_link(self, amount: int, comment: str):
        return f'https://lzt.market/balance/transfer?username={config.lolz_nick}&hold=0&amount={amount}&comment={comment}'

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'

    async def check_payment(self, amount: int, comment: str):
        user_id = config.lolz_id
        async with aiohttp.ClientSession(headers=self.session_headers, timeout=self.timeout) as session:
            response = await session.get(f'{self.api_url}market/user/{user_id}/payments', timeout=self.timeout)


            if response.status == 200:
                resp_json = await response.json()
                payments = resp_json['payments']
                for payment in payments.values():
                    if 'Перевод денег от' in payment['label']['title'] and int(amount) == payment['incoming_sum'] and comment == payment['data']['comment']:
                        await session.close()
                        return True
                await session.close()
                return False
            else:
                resp_text = await response.text()
                await session.close()
                error = resp_text
                error = error.split('<h1>')[1].split('</h1>')[0]
                return f"❗ Попробуйте чуть позже, {error}"