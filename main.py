import time
import datetime
from typing import Optional

from art import tprint

from app import run, is_delivery_time
from src.utils import Utils
from config import logger


class Run:
    def __init__(self):
        self.last_check: Optional[datetime.datetime] = None

    def main(self):
        tprint("PARSER SCRIPT", font="bulbhead")
        while True:
            run()
            if self.last_check is None or Utils.is_yesterday(date=self.last_check):
                is_delivery_time()
                self.last_check = datetime.datetime.now()
            logger.error("BOT SLEEP!")
            time.sleep(150)


if __name__ == '__main__':
    """Run script"""
    Run().main()
