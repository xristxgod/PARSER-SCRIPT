import datetime
from typing import List

from ..schemas import OrderData
from ..external import client
from ..inc import google_worker
from ..utils import utils


class GoogleSheetsAPIWorker:
    """GoogleSheetsAPIWorker - Working with data from Google Sheet"""

    @staticmethod
    def get_data(start: int = 1, end: int = 50, all_data: List = []) -> List[List]:
        """
        Get all the data from the table
        :param start: Where to start looking
        :param end: Where to finish the search
        :param all_data: Data is stored here
        :return: Data from the table
        """
        data = google_worker.get_data(start, end=end)
        if len(data) > 0:
            all_data.extend(data)
            return GoogleSheetsAPIWorker.get_data(start=end+1, end=end+51, all_data=all_data)
        return all_data

    @staticmethod
    def data_packaging(data: List[List]) -> List[OrderData]:
        """
        Pack the data into objects.
        :param data: Data from the table
        :return: Packed data
        """
        usd_to_rub_price = client.get_price("USD")
        return [
            OrderData(
                _id=user[0],
                orderId=user[1],
                priceUSD=float(user[2]),
                priceRUB=float(user[2]) * usd_to_rub_price,
                deliveryTime=utils.convert_time(user[3]) if not isinstance(user[3], datetime.datetime) else user[3]
            )
            for user in data
        ]


google_sheets_worker = GoogleSheetsAPIWorker
