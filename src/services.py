from datetime import datetime
from typing import Optional, List
from dataclasses import asdict

from .external import Client
from .inc import google_worker
from .schemas import DataOrder
from .utils import Utils


class Worker:
    @staticmethod
    def get_data(start: int = 1, end: int = 50, all_data: List = []) -> List[List]:
        data = google_worker.get_data(start, end=end)
        if len(data) > 0:
            all_data.extend(data)
            return Worker.get_data(start=end+1, end=end+51)
        return all_data

    @staticmethod
    def data_packaging(data: List[List]) -> List[DataOrder]:
        usd_to_rub_price = Client.get_price("USD")
        return [
            DataOrder(
                _id=user[0],
                orderId=user[1],
                priceUSD=float(user[2]),
                priceRUB=float(user[2]) * usd_to_rub_price,
                deliveryTime=Utils.convert_time(user[3])
            )
            for user in data
        ]


def run():
    pass