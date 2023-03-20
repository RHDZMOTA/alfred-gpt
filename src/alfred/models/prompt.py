import peewee

from alfred.models.user import User
from alfred.models.assistant import Assistant
from alfred.dao.interface import BaseModel


class Prompt(BaseModel):
    user = peewee.ForeignKeyField(
        User,
        backref="promts",
    )
    assistant = peewee.ForeignKeyField(
        Assistant,
        backref="requests",
    )
    content = peewee.TextField()
