from premium.logger import logging
from premium.exception import PremiumException
import os, sys

def test_logger_and_exception():
     try:
          logging.info("start testing logger and exception")
          result = 3/0
          print(result)
          logging.info("end testing logger and exception")
     except Exception as e:
          logging.debug("We are getting error over here")
          logging.info("We are getting error over here")
          raise PremiumException(e, sys)

if __name__=="__main__":
     try:
          test_logger_and_exception()
     except Exception as e:
          print(e)