from typing import Optional, List

from src.inc import google_worker


class Worker:
    @staticmethod
    def get_data(start: int = 1, end: int = 50, all_data: List = []) -> List[List]:
        data = google_worker.get_data(start, end=end)
        if len(data) > 0:
            all_data.extend(data)
            return Worker.get_data(start=end+1, end=end+51)
        return all_data

    @staticmethod
    def data_packaging(data: List[List]):
        pass
