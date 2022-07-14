from datetime import datetime
from typing import Optional, List
from dataclasses import asdict

from .inc import google_worker
from .schemas import DataOrder


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
        return [
            DataOrder(
                _id=user[0],
                orderId=user[1],
                priceUSD=float(user[2]),
                priceRUB="",
                deliveryTime=""
            )
            for user in data
        ]
