import requests
import xmltodict

from ..schemas import SendToTelegramData
from ..utils import utils
from config import Config


class Client:
    """Client - Working with external APIs"""
    @staticmethod
    def get_price(currency: str = "USD") -> float:
        """
        Get price by currency name
        Work with the Central Bank of the Russian Federation XML API
        :param currency: Currency name
        :return: Currency to RUB price
        """
        data = xmltodict.parse(
            requests.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={utils.get_time_now()}").text
        )
        price = list(filter(lambda x: x.get("CharCode") == currency.upper(), data['ValCurs']["Valute"]))[0]["Value"]
        return float(price.replace(',', "."))

    @staticmethod
    def send_to_telegram(data: SendToTelegramData) -> bool:
        """
        Send telegram bot info about delivery date
        :param data: Data for send to telegram bot information
        :return:
        """
        for chat_id in Config.TELEGRAM_ADMIN_IDS:
            requests.get(
                f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": (
                        "🔴 Delivery date passed!\n"
                        f"Planned delivery date: {data.deliveryTime.date()}\n"
                        f"Price: {data.priceUSD} USD | {data.priceRUB} RUB"
                    ),
                    "parse_mode": "html"
                }
            )
        return True


client = Client
