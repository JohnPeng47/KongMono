import logging
import json
from typing import Dict

from collections import defaultdict
from logging.handlers import RotatingFileHandler

class Stats:
    def __init__(self, file_handler: logging.Handler):
        self.logger = logging.getLogger("STATS")
        self.logger.setLevel(logging.INFO)

        # Create a stream handler for console output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.stats = {}

    def add_stat(self, key: str, value: Dict):
        if self.stats.get(key, None) is None:
            self.stats[key] = {}
        
        self.stats[key] = value

    def __str__(self):
        return json.dumps(self.stats, indent=2)