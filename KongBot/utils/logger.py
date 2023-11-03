import logging
from logging.handlers import RotatingFileHandler
from config import settings

def initialize_logging():
    create_base_logger()
    create_llm_logger()

def create_base_logger():
    """
    Base logger
    """
    logger = logging.getLogger("base")

    # configure for console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    # file handler
    file_handler = RotatingFileHandler(settings.LOG_FILE,
                                        maxBytes=10*1024*1024, 
                                        backupCount=5)
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    logger.setLevel(settings.LOG_LEVEL)
    file_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setLevel(settings.LOG_LEVEL)

    logger.propagate = False

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def create_llm_logger():
    """
    Logging LLM output
    """
    logger = logging.getLogger("llm")

    # file handler
    file_handler = RotatingFileHandler(settings.LLM_LOG_FILE,
                                        maxBytes=10*1024*1024, 
                                        backupCount=5)
    file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(module)s:%(funcName)s => %(message)s")
    )

    logger.setLevel(settings.LOG_LEVEL)
    file_handler.setLevel(settings.LOG_LEVEL)
    logger.addHandler(file_handler)
