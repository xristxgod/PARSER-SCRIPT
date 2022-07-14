from typing import List

from src.models import OrderModel
from src.services import Worker
from src.services.schemas import OrderData


def run():
    new_data: List[OrderData] = Worker.data_packaging(Worker.get_data())
    old_data: List[OrderData] = ...
