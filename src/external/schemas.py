import datetime
from dataclasses import dataclass


@dataclass()
class SendToTelegramData:
    orderId: int
    deliveryTime: datetime.datetime
    priceUSD: float
    priceRUB: float
