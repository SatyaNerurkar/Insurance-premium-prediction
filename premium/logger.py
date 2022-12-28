import os
import logging
from datetime import datetime

# Define log file name with current date and time stamp in hr min and sec.
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

# Define log directory inside current directory.
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

# create a folder if not already available
os.makedirs(LOG_FILE_DIR,exist_ok=True) 

# complete log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

# Setup basic configuration for logging.
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)