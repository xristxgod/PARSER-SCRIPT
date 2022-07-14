from typing import List, Set, Dict
from datetime import datetime

from ..services.schemas import OrderData


class Utils:
    @staticmethod
    def convert_time(date: str):
        return datetime.strptime(date, "%d.%m.%Y")

    @staticmethod
    def get_time_now() -> str:
        return datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def get_ids(data: List[OrderData]) -> Set[int]:
        return {_id._id for _id in data}

    @staticmethod
    def some_data(one_id: Set[int], two_id: Set[int], *, data: List[OrderData]) -> List[OrderData]:
        _ids = one_id.difference(two_id)
        _data = []
        for _id in _ids:
            d = list(filter(lambda x: x._id == _id, data))
            if len(d) == 1:
                _data.append(d[0])
        return _data
