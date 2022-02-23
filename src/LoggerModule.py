import logging
from datetime import datetime

log_format = "%(levelname)s %(asctime)s - %(message)s"
date = str(datetime.today().strftime("%b-%d-%Y"))

logging.basicConfig(filename = date + ".log",
                    filemode = "a",
                    format = log_format, 
                    level = logging.INFO)

logger = logging.getLogger()
