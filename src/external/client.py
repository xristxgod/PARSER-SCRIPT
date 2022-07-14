import requests
import xmltodict

from .schemas import SendToTelegramData
from ..utils import Utils


class Client:
    @staticmethod
    def get_price(currency: str = "USD") -> float:
        data = xmltodict.parse(
            requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={Utils.get_time_now()}").text
        )
        price = list(filter(lambda x: x.get("CharCode") == currency.upper(), data['ValCurs']["Valute"]))[0]["Value"]
        return float(price.replace(',', "."))

    @staticmethod
    def send_to_telegram(data: SendToTelegramData) -> bool:
        pass
