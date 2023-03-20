import datetime as dt

import peewee

from alfred.dao.database import db


class BaseModel(peewee.Model):
    created_at = peewee.DateTimeField(default=dt.datetime.utcnow, null=False)
    updated_at = peewee.DateTimeField(default=dt.datetime.utcnow, null=True)

    @classmethod
    def get_database(cls) -> peewee.Database:
        # Doing this for autocomplete reasons
        return getattr(getattr(cls, "_meta"), "database")

    class Meta:
        database = db
