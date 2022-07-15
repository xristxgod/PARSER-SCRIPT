import datetime
import time
from typing import Optional, Tuple, List, Dict

from art import tprint

from src import google_sheets_worker, client
from src.models import OrderModel, order_storage
from src.schemas import OrderData, OrderStorageData, OrderStorageUpdateData, SendToTelegramData
from src.utils import utils
from config import logger


class Demon:
    TIME_RUN = 150              # restart every 150 seconds

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Demon, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.last_check: Optional[datetime.datetime] = None

    def run(self):
        tprint("PARSER SCRIPT", font="bulbhead")
        while True:
            self.parser_script()
            if self.last_check is None or utils.is_yesterday(date=self.last_check):
                self.delivery_time_script()
                self.last_check = datetime.datetime.now()
            logger.error("BOT SLEEP!")
            time.sleep(10)

    # <<<==================================>>> Worker Parser script <<<==============================================>>>

    @staticmethod
    def get_data() -> Tuple:
        logger.info("TAKING DATA")
        new_data: List[OrderData] = google_sheets_worker.data_packaging(google_sheets_worker.get_data(all_data=[]))
        old_data: List[OrderData] = utils.convert_data(order_storage.read())
        if len(old_data) == 0:
            old_data: List[OrderData] = OrderModel.read()
            order_storage.create([
                OrderStorageData(
                    _id=d._id,
                    orderId=d.orderId,
                    priceUSD=d.priceUSD,
                    priceRUB=d.priceRUB,
                    deliveryTime=d.deliveryTime,
                    sentTelegram=False
                )
                for d in old_data
            ])
        if len(old_data) == 0:
            return new_data, None
        return new_data, old_data

    @staticmethod
    def cd_data(d1: List[Dict], d2: List[Dict], data: List[Dict]) -> List[Dict]:
        return utils.some_data(utils.get_ids(d1), utils.get_ids(d2), data=data)

    @staticmethod
    def update_data(new_data: List[Dict], old_data: List[Dict]):
        update_data = []
        for _id in utils.get_ids(new_data).intersection(utils.get_ids(old_data)):
            old = list(filter(lambda x: x.get("id") == _id, old_data))[0]
            new = list(filter(lambda x: x.get("id") == _id, new_data))[0]
            if old != new:
                update_data.append(new)
        return update_data

    @staticmethod
    def create_data(data: List[Dict]) -> Optional:
        if len(data) > 0:
            data_for_add = google_sheets_worker.data_packaging([list(d.values()) for d in data])
            status_sql = OrderModel.create(data_for_add)
            status_no_sql = order_storage.create(utils.convert_data_back(data_for_add))
            if status_sql and status_no_sql:
                logger.info(f"CREATE DATA: SUCCESSFULLY! IDS: {utils.get_ids(data)}")
            else:
                logger.error(f"CREATE DATA: BAD! IDS: {utils.get_ids(data)}")
        logger.error(f"DON'T HAVE CREATE DATA")

    @staticmethod
    def delete_data(data: List[Dict]) -> Optional:
        if len(data) > 0:
            data_for_delete = set(i.get("id") for i in data)
            status_sql = OrderModel.delete(data_for_delete)
            status_no_sql = order_storage.delete(data_for_delete)
            if status_sql and status_no_sql:
                logger.info(f"DELETE DATA: SUCCESSFULLY! IDS: {utils.get_ids(data)}")
            else:
                logger.error(f"DELETE DATA: BAD! IDS: {utils.get_ids(data)}")
        logger.error(f"DON'T HAVE DELETE DATA")

    @staticmethod
    def update_date(data: List[Dict]) -> Optional:
        if len(data) > 0:
            data_for_update = google_sheets_worker.data_packaging([list(d.values()) for d in data])
            status_sql = OrderModel.update(data_for_update)
            status_no_sql = order_storage.update(utils.convert_data_to_update(utils.convert_data_back(data_for_update)))
            if status_sql and status_no_sql:
                logger.info(f"UPDATE DATA: SUCCESSFULLY! IDS: {utils.get_ids(data)}")
            else:
                logger.error(f"UPDATE DATA: BAD! IDS: {utils.get_ids(data)}")
        logger.error(f"DON'T HAVE UPDATE DATA")

    @staticmethod
    def parser_script() -> Optional:
        """Parser | Google sheets => SQL DB"""
        logger.info("START NEW ITERATION")
        new_data, old_data = Demon.get_data()
        if old_data is None:
            logger.info("INIT ORDERS")
            OrderModel.create(data=new_data)
            order_storage.create(data=new_data)
            return None
        new_data: List[Dict] = [i.to_dict for i in new_data]
        old_data: List[Dict] = [i.to_dict for i in old_data]
        Demon.create_data(data=Demon.cd_data(new_data, old_data, new_data))
        Demon.delete_data(data=Demon.cd_data(old_data, new_data, old_data))
        Demon.update_date(data=Demon.update_data(new_data, old_data=old_data))

    # <<<==================================>>> Worker Parser script <<<==============================================>>>

    @staticmethod
    def delivery_time_script() -> Optional:
        all_data: List[OrderStorageData] = order_storage.read()
        update_data: List[OrderStorageUpdateData] = []
        for data in all_data:
            if not data.sentTelegram and utils.is_time(data.deliveryTime):
                logger.info(f"DELIVERY PASSED. ORDER: {data.orderId}")
                client.send_to_telegram(data=SendToTelegramData(
                    orderId=data.orderId,
                    deliveryTime=data.deliveryTime,
                    priceUSD=data.priceUSD,
                    priceRUB=data.priceRUB
                ))
                update_data.append(OrderStorageUpdateData(
                    _id=data._id,
                    sentTelegram=True,
                    deliveryTime=data.deliveryTime,
                    priceUSD=data.priceUSD
                ))
        order_storage.update(data=update_data)


if __name__ == '__main__':
    """Run script"""
    Demon().run()
