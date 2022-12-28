import os, sys
from premium.logger import logging
from premium.exception import PremiumException
from dotenv import load_dotenv

try:
    logging.info(f"Loading environment variable from .env file")
    load_dotenv()
except Exception as e:
    raise PremiumException(e, sys)