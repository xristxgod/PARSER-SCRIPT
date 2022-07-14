from typing import Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class OrderData:
    _id: int
    orderId: int
    priceUSD: float
    priceRUB: float
    deliveryTime: datetime

    @property
    def to_dict(self) -> Dict:
        return {
            "id": self._id, "order_id": self.orderId, "price_usd": self.priceUSD, "delivery_time": self.deliveryTime
        }
