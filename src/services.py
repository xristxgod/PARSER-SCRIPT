from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from config import Config, CREDENTIALS_CONFIG_FILE


class GoogleSheetsAPIWorker:
    __slots__ = (
        "__sample_spreadsheet_id", "__sample_range_name",
        "__sheet_id", "__credentials", "__service", "SCOPES"
    )
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets'
    ]

    def __init__(self):
        self.__sample_spreadsheet_id = Config.SAMPLE_SPREADSHEET_ID
        self.__sample_range_name = Config.SAMPLE_RANGE_NAME
        self.__sheet_id = Config.SHEET_ID
        self.__credentials = Credentials.from_service_account_file(CREDENTIALS_CONFIG_FILE, scopes=self.SCOPES)
        self.__service = build('sheets', 'v4', credentials=self.__credentials).spreadsheets()

    def get_data(self):
        pass
