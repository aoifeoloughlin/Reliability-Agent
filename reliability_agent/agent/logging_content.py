# logging_config.py
import logging
from agent.json_formatter import JsonFormatter
import sys

def get_logger():
    logger = logging.getLogger("agent")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger