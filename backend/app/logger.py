import logging
import sys
from app.settings import settings


def get_logger(module):
    log_format = "%(levelname)s | %(asctime)s | %(message)s"
    date_format = "%Y-%m-%d %a %H:%M:%S"
    log = logging.getLogger(module)

    try:
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        log_stream_handler = logging.StreamHandler(sys.stderr)
        log_stream_handler.setFormatter(formatter)
        log.addHandler(log_stream_handler)
    finally:
        # Avoid debug logs in production
        log.setLevel(logging.INFO if settings.PRODUCTION else logging.DEBUG)
        return log
