import os
import logging


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Config dir
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
# Credentials config file
CREDENTIALS_CONFIG_FILE = os.path.join(CONFIG_DIR, "credentials.json")


class Config:
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "13k0ORwAXAQ4LwaUGfReXmJ7x0SsXpHussJQZ-abm6lI")
    PAGE_NAME = os.getenv("PAGE_NAME", "test_page")
    SHEET_ID = os.getenv("SHEET_ID", "0")
