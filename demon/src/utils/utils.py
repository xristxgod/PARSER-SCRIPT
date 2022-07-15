from typing import List, Set, Dict
from datetime import datetime, timedelta

from ..schemas import OrderData, OrderStorageData, OrderStorageUpdateData


class Utils:
    """Utils - assistants at work"""
    @staticmethod
    def convert_time(date: str):
        """
        Convert from String to Datetime format
        :param date: Datetime in string
        :return: Datetime. Example format: 12.12.1999
        """
        return datetime.strptime(date, "%d.%m.%Y")

    @staticmethod
    def get_time_now() -> str:
        """
        Get time now for XML API params
        :return: String. Example format: 12/12/1999
        """
        return datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def is_time(date: datetime) -> bool:
        """
        Is there enough time
        :param date: Datetime
        :return: True or False
        """
        if datetime.now().date() > date.date():
            return True
        return False

    @staticmethod
    def is_yesterday(date: datetime) -> bool:
        """
        Is it more than yesterday's date or not?
        :param date: Datetime
        :return:
        """
        if date.date() + timedelta(days=1) == datetime.now().date():
            return True
        return False

    @staticmethod
    def get_ids(data: List[Dict]) -> Set[int]:
        """
        Get a set of IDs from orders.
        :param data: List of orders
        :return: Set of IDs
        """
        return {_id.get("id") for _id in data}

    @staticmethod
    def some_data(one_id: Set[int], two_id: Set[int], *, data: List[Dict]) -> List[Dict]:
        """
        Remove unnecessary data
        :param one_id: IDs of one group
        :param two_id: IDs of another group
        :param data: Data to change
        :return: Changed data
        """
        _ids = one_id.difference(two_id)
        _data = []
        for _id in _ids:
            d = list(filter(lambda x: x.get("id") == _id, data))
            if len(d) == 1:
                _data.append(d[0])
        return _data

    @staticmethod
    def convert_data(data: List[OrderStorageData]) -> List[OrderData]:
        return [
            OrderData(
                _id=d._id,
                orderId=d.orderId,
                priceUSD=d.priceUSD,
                priceRUB=d.priceRUB,
                deliveryTime=d.deliveryTime
            )
            for d in data
        ]

    @staticmethod
    def convert_data_back(data: List[OrderData]) -> List[OrderStorageData]:
        return [
            OrderStorageData(
                _id=d._id,
                orderId=d.orderId,
                priceUSD=d.priceUSD,
                priceRUB=d.priceRUB,
                deliveryTime=d.deliveryTime,
                sentTelegram=False
            )
            for d in data
        ]

    @staticmethod
    def convert_data_to_update(data: List[OrderStorageData]) -> List[OrderStorageUpdateData]:
        return [
            OrderStorageUpdateData(
                _id=d._id,
                priceUSD=d.priceUSD,
                deliveryTime=d.deliveryTime,
                sentTelegram=d.sentTelegram
            )
            for d in data
        ]


utils = Utils
