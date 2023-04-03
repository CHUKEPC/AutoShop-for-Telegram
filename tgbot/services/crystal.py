# - *- coding: utf- 8 - *-
import aiohttp

class CrystalPay:
    def __init__(self, login: str, token: str) -> None:
        self.login = login
        self.token = token
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.timeout = aiohttp.ClientTimeout(total=360)
        self.base_url = "https://api.crystalpay.io/v2"

    async def generate_pay_link(self, amount: int):
        try:
            async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
                url = f'{self.base_url}/invoice/create/'

                json = {
                "auth_login": self.login,
            "auth_secret": self.token,
            "amount": amount,
            "type": "purchase",
            "lifetime": 60
                }
                response = await session.post(url=url, json=json, timeout=self.timeout)
                res = await response.json()
                await session.close()
                return res
        except BaseException as err:
            print(err)
    async def get_pay_status(self, invoice_id: str):
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            url = f"{self.base_url}/invoice/info/"

            json = {
            "auth_login": self.login,
            "auth_secret": self.token,
            "id": invoice_id
            }

            response = await session.post(url=url, json=json, timeout=self.timeout)

            status = await response.json()
            await session.close()
            if status['state'] == "payed":
                return True
            else:
                return False

    async def get_balance(self):
        async with aiohttp.ClientSession(headers=self.headers, timeout=self.timeout) as session:
            json = {
                "auth_login": self.login,
                "auth_secret": self.token
            }
            response = await session.post(url=f"{self.base_url}/balance/info/", json=json, timeout=self.timeout)

            balances = await response.json()
            await session.close()

            bals = balances['balances']

            return f"""
<b>Bitcoin: <code>{bals['BITCOIN']['amount']} {bals['BITCOIN']['currency']}</code>
BnbSmartChain: <code>{bals['BNBSMARTCHAIN']['amount']} {bals['BNBSMARTCHAIN']['currency']}</code>
BtcBanker: <code>{bals['BTCBANKER']['amount']} {bals['BTCBANKER']['currency']}</code>
BtcChatex: <code>{bals['BTCCHATEX']['amount']} {bals['BTCCHATEX']['currency']}</code>
BtcCryptoBot: <code>{bals['BTCCRYPTOBOT']['amount']} {bals['BTCCRYPTOBOT']['currency']}</code>
CardRubP2P: <code>{bals['CARDRUBP2P']['amount']} {bals['CARDRUBP2P']['currency']}</code>
Dash: <code>{bals['DASH']['amount']} {bals['DASH']['currency']}</code>
EthBanker: <code>{bals['ETHBANKER']['amount']} {bals['ETHBANKER']['currency']}</code>
Ethereum: <code>{bals['ETHEREUM']['amount']} {bals['ETHEREUM']['currency']}</code>
LiteCoin: <code>{bals['LITECOIN']['amount']} {bals['LITECOIN']['currency']}</code>
LtcBanker: <code>{bals['LTCBANKER']['amount']} {bals['LTCBANKER']['currency']}</code>
LztMarket: <code>{bals['LZTMARKET']['amount']} {bals['LZTMARKET']['currency']}</code>
Polygon: <code>{bals['POLYGON']['amount']} {bals['POLYGON']['currency']}</code>
TonCryptoBot: <code>{bals['TONCRYPTOBOT']['amount']} {bals['TONCRYPTOBOT']['currency']}</code>
Tron: <code>{bals['TRON']['amount']} {bals['TRON']['currency']}</code>
USDCTrc: <code>{bals['USDCTRC']['amount']} {bals['USDCTRC']['currency']}</code>
USDTBanker: <code>{bals['USDTBANKER']['amount']} {bals['USDTBANKER']['currency']}</code>
USDTChatex: <code>{bals['USDTCHATEX']['amount']} {bals['USDTCHATEX']['currency']}</code>
USDTCryptoBot: <code>{bals['USDTCRYPTOBOT']['amount']} {bals['USDTCRYPTOBOT']['currency']}</code></b>
            """