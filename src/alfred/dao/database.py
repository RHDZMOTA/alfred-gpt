import peewee

from alfred.settings import (
    ALFRED_DEFAULT_SQLITE,
    get_logger,
)

logger = get_logger(name=__name__)


try:
    db: peewee.Database
    raise NotImplementedError
except NotImplementedError:
    logger.error("Database not implemented; using sqlite instead.")
    db = peewee.SqliteDatabase(ALFRED_DEFAULT_SQLITE)
except Exception as e:
    logger.error("Error encountered when trying to connect to database; falling back to sqlite database")
    logger.exception(e)
    db = peewee.SqliteDatabase(ALFRED_DEFAULT_SQLITE)
