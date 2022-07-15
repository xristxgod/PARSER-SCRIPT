"""`test_services.py` testing get_statistic_data from 'src/services.py'"""
from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch


from src.services import get_statistic_data


class TestServices(unittest.TestCase):
    @patch("src.services.get_orders")
    def test_get_statistic_data(self, get_orders: Mock):
        get_orders.return_value = [
            (555.12, datetime.now()),
            (124.44, datetime.now() + timedelta(days=12))
        ]
        result = get_statistic_data()
        assert isinstance(result, tuple)
        assert isinstance(result[0], list)
        assert isinstance(result[0][0], str) and isinstance(result[1][0], float)
