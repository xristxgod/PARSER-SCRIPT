from datetime import datetime


class Utils:
    @staticmethod
    def convert_time(date: str):
        return datetime.strptime(date, "%d.%m.%Y")

    @staticmethod
    def get_time_now() -> str:
        return datetime.now().strftime("%d/%m/%Y")
