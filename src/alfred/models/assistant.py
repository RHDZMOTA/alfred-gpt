import peewee

from alfred.models.user import User
from alfred.models.fields import GenderField
from alfred.resources import ResourceManager
from alfred.dao.interface import BaseModel


class Assistant(BaseModel):
    user = peewee.ForeignKeyField(
        User,
        backref="assistant",
        unique=True
    )
    name = peewee.TextField(
        default="Alfred",
    )
    gender = GenderField(
        default=GenderField.get_catalog().UNDEFINED,
        null=False
    )
    description = peewee.TextField(
        null=False,
        default=ResourceManager.get("assistant_description.txt")
    )
