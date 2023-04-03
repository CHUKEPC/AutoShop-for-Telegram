import aiohttp
from datetime import datetime, timedelta, timezone

class Qiwi:
    def __init__(self, token, number, p2p_token) -> None:
        self.token = token
        self.number = number
        self.p2p_token = p2p_token
        self.session_headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.p2p_headers = {
            "Authorization": f"Bearer {self.p2p_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.timeout = aiohttp.ClientTimeout(total=360)

    @staticmethod
    async def convert_date(lifetime: int):
        datetime_new: datetime = datetime.now(timezone(timedelta(hours=3))).replace(microsecond=0)
        datetime_new = datetime_new + timedelta(minutes=lifetime)

        return datetime_new.astimezone(timezone(timedelta(hours=3))).replace(microsecond=0).isoformat()

    async def create_bill(self, amount, comment):
        async with aiohttp.ClientSession(headers=self.p2p_headers, timeout=self.timeout) as session:
            url = f"https://api.qiwi.com/partner/bill/v1/bills/{comment}"

            params = {
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "expirationDateTime": await self.convert_date(60)
            }

            response = await session.put(url=url, json=params, timeout=self.timeout)
            resp = await response.json()
            await session.close()
            return resp

    async def check_bill(self, bill_id):
        async with aiohttp.ClientSession(headers=self.p2p_headers, timeout=self.timeout) as session:
            url = f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}"
            data = {
                "type": "money_transfer",
                "is_hold": 0
            }
            response = await session.get(url=url, timeout=self.timeout, data=data)

            bill = await response.json()
            await session.close()
            if bill['status']['value'] == "PAID":
                return True
            else:
                return False
        
    async def get_balance(self, number):
        async with aiohttp.ClientSession(headers=self.session_headers, timeout=self.timeout) as session:
            url = f"https://edge.qiwi.com/funding-sources/v2/persons/{number}/accounts"

            resp = await session.get(url=url)

            response = await resp.json()
            await session.close()
            bal = []

            for balance in response['accounts']:
                if "qw_wallet_usd" == balance['alias']:
                    bal.append(f"$: <code>{balance['balance']['amount']}$</code>")

                if "qw_wallet_rub" == balance['alias']:
                    bal.append(f"RUB: <code>{balance['balance']['amount']} RUB</code>")

                if "qw_wallet_kzt" == balance['alias']:
                    bal.append(f"₸: <code>{balance['balance']['amount']}₸</code>")

            bal = "\n".join(bal)

            return bal