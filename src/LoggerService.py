import logging
from datetime import datetime

# logging library is used with a certain format
# a new file is written every day with the date as filename
# new log messages will be appended to the existing file

log_format = "%(levelname)s %(asctime)s - %(message)s"
date = str(datetime.today().strftime("%b-%d-%Y"))

logging.basicConfig(filename = date + ".log",
                    filemode = "a",
                    format = log_format, 
                    level = logging.INFO)

logger = logging.getLogger()
