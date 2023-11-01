import logging
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.DEBUG

def create_logger():
    logger = logging.getLogger("logger")
    logger.setLevel(LOG_LEVEL)

    # configure for console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )
    
    # file handler
    file_handler = RotatingFileHandler(r"C:\Users\jpeng\Documents\business\kongyiji\kongbot\output.log",
                                        maxBytes=10*1024*1024, 
                                        backupCount=5)
    file_handler.setFormatter(
        logging.Formatter("HELLWOORLD[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

