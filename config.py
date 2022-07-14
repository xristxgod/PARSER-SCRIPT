import os
import logging


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Config dir
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
# Credentials config file
CREDENTIALS_CONFIG_FILE = os.path.join(CONFIG_DIR, "credentials.json")


logger = logging.getLogger(__name__)
logging.basicConfig(
    format=u"[%(asctime)s][%(filename)s][LINE:%(lineno)d][%(levelname)s] | %(message)s",
    level=logging.INFO
)


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "5547645946:AAE18qQ070Nk7GhJHZ_R58N0indHhCKxreg")
    TELEGRAM_ADMIN_IDS = os.getenv("TELEGRAM_ADMIN_IDS", "688225742,").split(",")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(CONFIG_DIR, 'db.db')}")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "13k0ORwAXAQ4LwaUGfReXmJ7x0SsXpHussJQZ-abm6lI")
    PAGE_NAME = os.getenv("PAGE_NAME", "test_page")
    SHEET_ID = os.getenv("SHEET_ID", "0")
