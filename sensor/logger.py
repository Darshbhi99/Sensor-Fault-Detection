'''
This is the python file for creating and adding logs of every step of the code
'''
import logging
import os
from datetime import datetime
from from_root import from_root

# Gave the name for the logger file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Setting the path for the log directory and file
logs_path = os.path.join(from_root(), "logs", LOG_FILE)

# Making the log directory
os.makedirs(logs_path, exist_ok=True)

# Log file path 
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Adding the Data to the log file 
logging.basicConfig(
    filename= LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)
