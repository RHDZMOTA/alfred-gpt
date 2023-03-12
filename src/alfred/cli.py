import datetime as dt
from time import perf_counter
from typing import Optional
from types import TracebackType
from dataclasses import dataclass, field

from .settings import get_logger
from .models import Status


logger = get_logger(name=__name__)


@dataclass(slots=True)
class CLI:
    execution_time: dt.datetime = field(default_factory=dt.datetime.utcnow)
    perfc: float = field(default_factory=perf_counter)

    def __enter__(self):
        logger.info("Initializing Alfred...")
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ):
        status = Status.from_bool(exc_val is None)
        logger.info("Command execution status: %s", status.value)
        logger.info("Command execution duration: %f", perf_counter() - self.perfc)

    def hello(self, world: Optional[str] = None) -> str:
        return f"Hello, {world or 'world'}!"
