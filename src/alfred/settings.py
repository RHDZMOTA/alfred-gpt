import os
import logging
from typing import Optional


ALFRED_LOG_LEVEL = os.environ.get(
    "ALFRED_LOG_LEVEL",
    default="INFO",
).strip()


def get_logger(name: str, level: Optional[str] = None):
    logging.basicConfig(
        level=level or ALFRED_LOG_LEVEL
    )
    logger = logging.getLogger(name=name)
    return logger
