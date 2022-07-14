import datetime
from typing import Union, List, Set

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
            return Worker.get_data(start=end+1, end=end+51, all_data=all_data)
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
    def create(data: List[OrderData]) -> bool:
        try:
            _ = [session.add(OrderModel(**d.to_dict)) for d in data]
            session.commit()
            return True
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
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

    @staticmethod
    def update(data: List[OrderData]) -> bool:
        try:
            for d in data:
                order: OrderModel = session.query(OrderModel).get(d._id)
                order.order_id = d.orderId
                order.price_usd = d.priceUSD
                order.delivery_time = d.deliveryTime
            session.commit()
            return True
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def delete(ids: Set[int]) -> bool:
        try:
            [session.delete(session.query(OrderModel).get(_id)) for _id in ids]
            session.commit()
            return True
        except Exception as error:
            logger.error(f"{error}")
            session.rollback()
            return False
        finally:
            session.close()
