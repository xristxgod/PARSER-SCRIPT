from typing import Union, Optional, List, Set, Dict
from dataclasses import asdict

import pymongo
import sqlalchemy
from sqlalchemy import Column, orm
from sqlalchemy.types import BigInteger, DateTime, Float
from sqlalchemy_utils import database_exists, create_database

from .base import StaticCRUD, CRUD
from .schemas import OrderData, OrderStorageData, OrderStorageUpdateData
from .services import google_sheets_worker
from .utils import utils
from config import Config, logger


# <<<============================================>>> SQL <<<=========================================================>>>


BaseModel = orm.declarative_base()
engine = sqlalchemy.create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})
if not database_exists(engine.url):
    create_database(engine.url)
session = orm.Session(engine)


class OrderModel(BaseModel, StaticCRUD):
    __tablename__ = "order_model"
    id = Column(BigInteger, primary_key=True, unique=True)
    order_id = Column(BigInteger, unique=True)
    price_usd = Column(Float, default=0)
    price_rub = Column(Float, default=0)
    delivery_time = Column(DateTime, default=utils.get_time_now())

    def __repr__(self):
        return f"{self.order_id}"

    @property
    def to_list(self) -> List:
        return [self.id, self.order_id, self.price_usd, self.delivery_time]

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
        """
        Get data by id or get all data if don't get id
        :param _id: Order id
        :return: Order/s data
        """
        try:
            if _id is None:
                return google_sheets_worker.data_packaging([data.to_list for data in session.query(OrderModel).all()])
            return google_sheets_worker.data_packaging(session.query(OrderModel).get(12).to_list)
        except Exception as error:
            logger.error(f"{error}")
        finally:
            session.close()

    @staticmethod
    def update(data: List[OrderData]) -> bool:
        """
        Update order/s
        :param data: Data for id
        :return: True of False
        """
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
        """
        Delete order/s
        :param ids: Order id/s
        :return: True of False
        """
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


def create_db():
    BaseModel.metadata.create_all(engine)


# <<<============================================>>> NoSQL <<<=======================================================>>>

class BaseStorage:
    """BaseStorage - Parent class for working with MongoDB collections"""
    __slots__ = ("client", "db", "__collection")

    def __init__(self):
        self.client = pymongo.MongoClient(Config.MONGODB_URL)  # Client session
        self.db = self.client[Config.MONGODB_NAME]  # Connect to db
        self.__collection: Optional[pymongo.collection.Collection] = None

    def __del__(self):
        """Delete MongoDB connections after stopping the bot."""
        self.client.close()

    @property
    def url(self) -> str:
        """Path to MongoDB"""
        return f"{self.client.HOST}:{self.client.PORT}"


class OrderStorage(BaseStorage, CRUD):
    """Language model - Remembers the user language state"""
    __slots__ = tuple()

    def __init__(self, collection_name: str = "secret"):
        """
        Work to mangodb
        :param collection_name: Name for collection
        Format data:
        {
            "_id": int,
            "orderId": int,
            "priceUSD": float
            "priceRUB": float
            "deliveryTime": str
            "sentTelegram": bool
        }
        """
        super(OrderStorage, self).__init__()
        self.__collection = self.db[collection_name]

    @property
    def collection(self) -> str:
        """Collection name"""
        return self.__collection.name

    @property
    def all_data(self) -> List[Dict]:
        """Show all data in collection"""
        if self.__collection is not None:
            return [data for data in self.__collection.find()]
        return []

    def create(self, data: List[OrderStorageData]) -> bool:
        """Create new order"""
        try:
            for d in data:
                self.__collection.insert_one(asdict(d))
            return True
        except Exception as error:
            logger.error(f"{error}")
            return False

    def read(self, _id: int = None) -> Union[List[OrderStorageData], OrderStorageData]:
        """Get order by id"""
        try:
            if _id is not None:
                return OrderStorageData(**{
                    key: value
                    for key, value in self.__collection.find_one({"_id": _id}).items()
                    if key in OrderStorageData.keys()
                })
            return [OrderStorageData(**data) for data in self.all_data]
        except AttributeError:
            return []
        except Exception as error:
            logger.error(f"{error}")
            return []

    def update(self, data: List[OrderStorageUpdateData]) -> bool:
        """Update order by id"""
        try:
            for d in data:
                self.__collection.update_one({"_id": d._id}, {"$set": d.to_dict})
            return True
        except Exception as error:
            logger.error(f"{error}")
            return False

    def delete(self, ids: List[int]) -> bool:
        """Delete order bu id"""
        try:
            for _id in ids:
                self.__collection.delete_one({"_id": _id})
            return True
        except Exception as error:
            logger.error(f"{error}")
            return False


order_storage = OrderStorage(collection_name="order_model")
