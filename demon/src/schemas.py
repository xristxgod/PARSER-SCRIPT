import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass, field


@dataclass()
class OrderData:
    _id: int                            # ID in DB
    orderId: int                        # Order id
    priceUSD: float                     # Price in USD
    priceRUB: float                     # Price in RUB
    deliveryTime: datetime              # Delivery time

    @property
    def to_dict(self) -> Dict:
        return {
            "id": int(self._id), "order_id": int(self.orderId),
            "price_usd": float(self.priceUSD), "delivery_time": self.deliveryTime
        }


@dataclass()
class SendToTelegramData:
    orderId: int                        # Order id
    deliveryTime: datetime.datetime     # Delivery time
    priceUSD: float                     # Price in USD
    priceRUB: float                     # Price in RUB


@dataclass()
class OrderStorageData:
    _id: int                                               # ID in DB
    orderId: int                                           # Order id
    priceUSD: float                                        # Price in USD
    priceRUB: float                                        # Price in RUB
    deliveryTime: datetime                                 # Delivery time
    sentTelegram: Optional[bool] = field(default=False)    # Sent to telegram if delivery time passed

    @staticmethod
    def keys() -> List:
        return ["id", "orderId", "priceUSD", "priceRUB", "deliveryTime", "sentTelegram"]


@dataclass()
class OrderStorageUpdateData:
    _id: int                                                            # Order id
    priceUSD: Optional[float] = field(default=None)                     # Price in USD
    deliveryTime: Optional[datetime.datetime] = field(default=None)     # Delivery time
    sentTelegram: Optional[bool] = field(default=None)                  # Sent to telegram if delivery time passed

    @property
    def to_dict(self) -> Dict:
        return {
            "priceUSD": self.priceUSD, "deliveryTime": self.deliveryTime, "sentTelegram": self.sentTelegram
        }
