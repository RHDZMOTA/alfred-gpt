import datetime as dt

import peewee
from peewee import (
    SqliteDatabase,
    DateTimeField,
    Model,
)

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
    db = SqliteDatabase(ALFRED_DEFAULT_SQLITE)
except Exception as e:
    logger.error("Error encountered when trying to connect to database; falling back to sqlite database")
    logger.exception(e)
    db = SqliteDatabase(ALFRED_DEFAULT_SQLITE)


class BaseModel(Model):
    created_at = DateTimeField(default=dt.datetime.utcnow, null=False)
    updated_at = DateTimeField(default=dt.datetime.utcnow, null=True)

    @classmethod
    def get_database(cls) -> peewee.Database:
        # Doing this for autocomplete reasons
        return getattr(getattr(cls, "_meta"), "database")

    class Meta:
        database = db
