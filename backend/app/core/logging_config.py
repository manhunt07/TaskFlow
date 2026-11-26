import json
import logging
import sys

from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format application logs as structured JSON."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "level": record.levelname,

            "logger": record.name,

            "event": record.getMessage(),
        }

        # Include only approved fields.
        allowed_fields = (
            "request_id",
            "method",
            "path",
            "status_code",
            "duration_ms",
            "exception_type",
        )

        for field in allowed_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        return json.dumps(log_data)


def setup_logging():
    """Configure TaskFlow application request logging."""

    logger = logging.getLogger("taskflow.requests")

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers when setup runs again.
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        handler.setFormatter(JSONFormatter())

        logger.addHandler(handler)

    logger.propagate = False

    return logger
