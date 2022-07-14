import json
from typing import Optional, List, Dict

from src.services import Worker, OrderController
from src.utils import Utils
from src.services.schemas import OrderData
from config import logger


def run() -> Optional:
    logger.info("START NEW ITERATION")
    new_data: List[OrderData] = Worker.data_packaging(Worker.get_data())
    old_data: List[OrderData] = OrderController.read()
    if len(old_data) == 0:
        logger.info("INIT ORDERS")
        OrderController.create(data=new_data)
        return
    new_data: List[Dict] = [i.to_dict for i in new_data]
    old_data: List[Dict] = [i.to_dict for i in old_data]
    create_data = Utils.some_data(Utils.get_ids(new_data), Utils.get_ids(old_data), data=new_data)
    logger.info(f"CREATE DATA. IDS: {Utils.get_ids(create_data)}" if len(create_data) > 0 else "NOT CREATE")
    delete_data = Utils.some_data(Utils.get_ids(old_data), Utils.get_ids(new_data), data=old_data)
    logger.info(f"DELETE DATA. IDS: {Utils.get_ids(delete_data)}" if len(delete_data) > 0 else "NOT DELETE")
    update_data = []
    for _id in Utils.get_ids(new_data).intersection(Utils.get_ids(old_data)):
        old = list(filter(lambda x: x.get("id") == _id, old_data))[0]
        new = list(filter(lambda x: x.get("id") == _id, new_data))[0]
        if old != new:
            update_data.append(new)
            break
    logger.info(f"UPDATE DATA. IDS: {Utils.get_ids(update_data)}" if len(update_data) > 0 else "NOT UPDATE")
    if len(create_data) > 0:
        try:
            if not OrderController.create(Worker.data_packaging([list(data.values()) for data in create_data])):
                raise Exception
            logger.info(f"CREATE DATA: SUCCESSFULLY! IDS: {Utils.get_ids(create_data)}")
        except Exception as error:
            logger.error(f"{error} | CREATE DATA: BAD! IDS: {Utils.get_ids(create_data)}")
    if len(delete_data) > 0:
        try:
            if not OrderController.delete(Utils.get_ids(delete_data)):
                raise Exception
            logger.info(f"DELETE DATA: SUCCESSFULLY! IDS: {Utils.get_ids(delete_data)}")
        except Exception as error:
            logger.error(f"{error} | DELETE DATA: BAD! IDS: {Utils.get_ids(delete_data)}")
    if len(update_data) > 0:
        try:
            if not OrderController.update(Worker.data_packaging([list(data.values()) for data in update_data])):
                raise Exception
            logger.info(f"UPDATE DATA: SUCCESSFULLY! IDS: {Utils.get_ids(update_data)}")
        except Exception as error:
            logger.error(f"{error} | UPDATE DATA: BAD! IDS: {Utils.get_ids(update_data)}")


if __name__ == '__main__':
    """Run one iteration"""
    run()
