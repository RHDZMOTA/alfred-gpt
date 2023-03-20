import peewee

from alfred.models.prompt import Prompt
from alfred.dao.interface import BaseModel


class Response(BaseModel):
    prompt = peewee.ForeignKeyField(
        Prompt,
        backref="responses",
    )
    content = peewee.TextField()
