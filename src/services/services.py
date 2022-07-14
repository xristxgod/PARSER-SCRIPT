import datetime
from typing import Union, List

from .schemas import OrderData
from ..models import OrderModel, session
from ..external import Client
from ..inc import google_worker
from ..utils import Utils
from config import logger


class Worker:
    @staticmethod
    def get_data(start: int = 1, end: int = 50, all_data: List = []) -> List[List]:
        data = google_worker.get_data(start, end=end)
        if len(data) > 0:
            all_data.extend(data)
            return Worker.get_data(start=end+1, end=end+51)
        return all_data

    @staticmethod
    def data_packaging(data: List[List]) -> List[OrderData]:
        usd_to_rub_price = Client.get_price("USD")
        return [
            OrderData(
                _id=user[0],
                orderId=user[1],
                priceUSD=float(user[2]),
                priceRUB=float(user[2]) * usd_to_rub_price,
                deliveryTime=Utils.convert_time(user[3]) if not isinstance(user[3], datetime.datetime) else user[3]
            )
            for user in data
        ]


class OrderController:
    @staticmethod
    def create(data: Union[List[OrderData], OrderData]) -> bool:
        try:
            if isinstance(data, list):
                [session.add(OrderModel(**d.to_dict)) for d in data]
            else:
                session.add(OrderModel(**data.to_dict))
            session.commit()
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def read(_id: int = None) -> Union[List[OrderData], OrderData]:
        try:
            if _id is None:
                return Worker.data_packaging([data.to_list for data in session.query(OrderModel).all()])
            return Worker.data_packaging(session.query(OrderModel).get(12).to_list)
        except Exception as error:
            logger.error(f"{error}")
        finally:
            session.close()
