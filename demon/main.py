from app import Demon
from src.models import create_db
from config import logger


if __name__ == '__main__':
    """Run script"""
    try:
        create_db()
    except Exception as error:
        logger.error(f"{error}")
    Demon().run()
