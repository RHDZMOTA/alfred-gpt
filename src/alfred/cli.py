import datetime as dt
from time import perf_counter
from types import TracebackType
from dataclasses import dataclass, field
from typing import (
    Optional,
)

from alfred.models import ModelRegistry
from alfred.models.enums import Status
from alfred.settings import get_logger


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

    def find_models(self, sep: Optional[str] = None) -> str:
        sep = f"\n{sep or '-'} "
        return sep + sep.join(
            model.__name__
            for model in ModelRegistry.find_all()
        )

    def setup(self, reset: bool = False):
        # Create backend tables
        logger.info("Working on setting up the backend database...")
        from alfred.dao.database import db

        table_registry = ModelRegistry.find_all()
        logger.info("Models found: %d", len(table_registry))
        logger.debug(
            "Models: %s",
            " ".join(cls.__name__ for cls in table_registry)
        )
        with db:
            not reset or db.drop_tables(models=table_registry)
            db.create_tables(models=table_registry)
