import textwrap
import datetime as dt
from time import perf_counter
from types import TracebackType
from tempfile import NamedTemporaryFile
from dataclasses import dataclass, field
from typing import (
    Callable,
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

    @staticmethod
    def _display_values(
            *args,
            sep: Optional[str] = None,
            apply: Optional[Callable] = None
    ):
        apply = apply or (lambda arg: arg)
        sep = f"\n{sep or '-'} "
        print(sep + sep.join(apply(arg) for arg in args))

    def find_views(self, sep: Optional[str] = None):
        from alfred.frontend.controller import ViewController

        self._display_values(
            *ViewController.instance().views.keys(),
            sep=sep,
        )

    def find_models(self, sep: Optional[str] = None):
        self._display_values(
            *ModelRegistry.find_all(),
            sep=sep,
            apply=lambda model: model.__name__
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

    def frontend(
            self,
            view: Optional[str] = None,
            output_path: Optional[str] = None,
            port: Optional[str] = None,
    ):
        from alfred.frontend import runner

        view = view or "about"
        with NamedTemporaryFile(mode="r+", delete=False, dir=output_path, suffix=".py") as file:
            file.write(
                textwrap.dedent(
                    f"""
                    from alfred.frontend.controller import ViewController
                    
                    if __name__ == "__main__":
                        controller = ViewController.instance()
                        controller.run(view_name={repr(view)})
                    """
                )
            )

        runner(temp_file=file.name, port=port)
