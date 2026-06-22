# logging_config.py
import logging
from agent.JsonFormatter import JsonFormatter
import sys

def get_logger():
    if not logger.handlers:
        logger = logging.getLogger("agent")
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.propagate = False
    return logger