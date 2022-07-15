from typing import List
from datetime import datetime
import unittest
from unittest.mock import Mock, patch

from src.schemas import OrderData
from src.services.services import google_sheets_worker


class TestServices(unittest.TestCase):
    @patch("src.external.client.get_price")
    def test_data_packaging(self, get_price: Mock):
        get_price.return_value = 58.32
        result: List[OrderData] = google_sheets_worker.data_packaging(data=[
            [
                1, 1244, 233, "12.12.1999",
            ],
            [
                2, 2223, 144, datetime.now()
            ]
        ])
        assert isinstance(result, list)
        assert isinstance(result[0], OrderData)
        assert result[0].orderId == 1244 and result[1].orderId == 2223
        assert isinstance(result[0].deliveryTime, datetime)
