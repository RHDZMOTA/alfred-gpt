import os
import logging
from typing import List, Optional


ALFRED_LOG_LEVEL = os.environ.get(
    "ALFRED_LOG_LEVEL",
    default="INFO",
).strip()

ALFRED_ACTIVATION_CODES: List[str] = os.environ.get(
    "ALFRED_ACTIVATION_CODES",
    default=""
).split(":")

ALFRED_SECRET = os.environ.get(
    "ALFRED_SECRET",
    default="",
)


ALFRED_DEFAULT_SALT_LENGTH: int = int(os.environ.get(
    "ALFRED_DEFAULT_SALT_LENGTH",
    default=5,
))

ALFRED_DEFAULT_SQLITE = os.environ.get(
    "ALFRED_DEFAULT_SQLITE",
    default="alfred.db"
)


def get_logger(name: str, level: Optional[str] = None):
    logging.basicConfig(
        level=level or ALFRED_LOG_LEVEL
    )
    logger = logging.getLogger(name=name)
    return logger


_logger = get_logger(name=__name__)


if not ALFRED_SECRET:
    _logger.error("Alfred Secret environ.var was not provided.")
