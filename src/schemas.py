from dataclasses import dataclass
from datetime import datetime


@dataclass()
class DataOrder:
    _id: int
    orderId: int
    priceUSD: float
    priceRUB: float
    deliveryTime: datetime
