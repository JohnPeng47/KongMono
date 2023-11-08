from config import settings

from logging import StreamHandler, Formatter, Logger
from logging.handlers import RotatingFileHandler

def configure_logger(logger: Logger):
    logger.setLevel(settings.SERVER_LOG_LEVEL)

    # configure for console logging
    console_handler = StreamHandler()
    console_handler.setFormatter(
        Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    # file handler
    file_handler = RotatingFileHandler(settings.SERVER_LOG_FILE,
                                        maxBytes=10*1024*1024, 
                                        backupCount=5)
    file_handler.setFormatter(
        Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
