import os
import logging


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Config dir
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
# Credentials config file
CREDENTIALS_CONFIG_FILE = os.path.join(CONFIG_DIR, "credentials.json")


class Config:
    SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
    SAMPLE_RANGE_NAME = os.getenv("SAMPLE_RANGE_NAME")
    SHEET_ID = os.getenv("SHEET_ID")
