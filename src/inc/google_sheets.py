from typing import List

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from config import Config, CREDENTIALS_CONFIG_FILE


class GoogleSheetsAPIWorker:
    SPREADSHEET_ID = Config.SPREADSHEET_ID                      # Spreadsheets id. In params: .../spreadsheets/<this>/..
    PAGE_NAME = Config.PAGE_NAME                                # Page name. Example: List1, List2
    SHEET_ID = Config.SHEET_ID                                  # Sheets id. In params: .../edit#gid=0
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GoogleSheetsAPIWorker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__credentials: Credentials = Credentials.from_service_account_file(CREDENTIALS_CONFIG_FILE, scopes=self.SCOPES)
        self.__service = build('sheets', 'v4', credentials=self.__credentials).spreadsheets()

    def get_data(self, start: int = 1, end: int = 50) -> List[List]:
        return self.__service.values().get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{self.PAGE_NAME}!A{start+1}:D{end+1}"
        ).execute().get("values", [])


google_worker = GoogleSheetsAPIWorker()
