from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch

from src.utils.utils import utils


class TestUtils(unittest.TestCase):
    def test_convert_time(self):
        result = utils.convert_time("12.12.1999")
        assert isinstance(result, datetime)

    def test_get_time_now(self):
        result: str = utils.get_time_now()
        assert isinstance(result, str)

    def test_is_time(self):
        result = utils.is_time(date=datetime.now())
        assert isinstance(result, bool)
        assert result is False

    def test_is_yesterday(self):
        result = utils.is_yesterday(date=datetime.now() - timedelta(days=1))
        assert isinstance(result, bool)
        assert result is True

    def test_get_ids(self):
        result = utils.get_ids(data=[
            {"id": 12, "data": "gigi"},
            {"id": 23, "data": "murad"}
        ])
        assert isinstance(result, set)
        assert len(result) == 2

    def test_some_data(self):
        pass

    def test_convert_data(self):
        pass

    def test_convert_data_back(self):
        pass

    def test_convert_data_to_update(self):
        pass
