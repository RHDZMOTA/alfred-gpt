import peewee

from alfred.models.user import User
from alfred.dao.interface import BaseModel
from alfred.models.fields import (
    GenderField,
    LangField,
)


class UserProfile(BaseModel):
    user = peewee.ForeignKeyField(
        User,
        backref="profile",
        unique=True,
    )
    birthdate = peewee.DateTimeField(
        null=False,
    )
    gender = GenderField(
        null=False,
    )
    lang = LangField(
        null=False,
        default=LangField.get_catalog().ALL,
    )
    description = peewee.TextField(
        null=False,
    )
    profession_title = peewee.TextField(
        null=True,
    )
    profession_description = peewee.TextField(
        null=True,
    )
