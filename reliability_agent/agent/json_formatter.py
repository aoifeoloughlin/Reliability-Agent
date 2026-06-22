import logging, json, sys
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        extra_fields = {
            k: v for k, v in data.items()
            if k not in logging.LogRecord("", "", "", "", "", (), {}).__dict__
        }

        log_object.update(extra_fields)

        return json.dumps(log_object)
