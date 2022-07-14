from typing import List, Set, Dict
from datetime import datetime, timedelta


class Utils:
    @staticmethod
    def convert_time(date: str):
        return datetime.strptime(date, "%d.%m.%Y")

    @staticmethod
    def get_time_now() -> str:
        return datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def is_time(date: datetime) -> bool:
        if datetime.now().date() > date.date():
            return True
        return False

    @staticmethod
    def is_yesterday(date: datetime) -> bool:
        # if (date + timedelta(days=1)).strftime("%d.%m.%Y") == datetime.now().strftime("%d.%m.%Y"):
        if date.date() + timedelta(days=1) == datetime.now().date():
            return True
        return False

    @staticmethod
    def get_ids(data: List[Dict]) -> Set[int]:
        return {_id.get("id") for _id in data}

    @staticmethod
    def some_data(one_id: Set[int], two_id: Set[int], *, data: List[Dict]) -> List[Dict]:
        _ids = one_id.difference(two_id)
        _data = []
        for _id in _ids:
            d = list(filter(lambda x: x.get("id") == _id, data))
            if len(d) == 1:
                _data.append(d[0])
        return _data
