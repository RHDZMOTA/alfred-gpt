import peewee

from alfred.backend.database import BaseModel
from alfred.backend.fields import (
    GenderField,
    LangField,
)
from alfred.settings import (
    ALFRED_ACTIVATION_CODES,
    get_logger,
)
from alfred.resources import ResourceManager
from alfred.utils import password_cooking


logger = get_logger(name=__name__)


class User(BaseModel):
    name = peewee.CharField(null=False, unique=True)
    email = peewee.CharField(null=False, unique=True)
    password_hash = peewee.CharField(null=False)
    password_salt = peewee.CharField(null=False)
    verified = peewee.BooleanField(default=False, null=False)

    @classmethod
    def create(
            cls,
            activation_code: str,
            password: str,
            name: str,
            email: str,
    ):

        if activation_code not in ALFRED_ACTIVATION_CODES:
            logger.error("Invalid activation code provided: %s", activation_code)
            return
        pwd_hash, pwd_salt = password_cooking(pwd=password)
        # https://peewee.readthedocs.io/en/latest/peewee/models.html#model-options-and-table-metadata
        with cls.get_database().atomic():
            return super().create(
                name=name,
                email=email,
                password_hash=pwd_hash,
                password_salt=pwd_salt,
                verified=False,
            )


class UserProfile(BaseModel):
    user = peewee.ForeignKeyField(User, backref="profile", unique=True)
    birthdate = peewee.DateTimeField(null=False)
    gender = GenderField(null=False)
    lang = LangField(null=False, default=LangField.Enum.EN)
    description = peewee.TextField(null=False)
    profession_title = peewee.TextField(null=True)
    profession_description = peewee.TextField(null=True)


class Assistant(BaseModel):
    user = peewee.ForeignKeyField(User, backref="assistant", unique=True)
    name = peewee.TextField(default="Alfred", )
    gender = GenderField(default=GenderField.Enum.UNDEFINED, null=False)
    description = peewee.TextField(
        null=False,
        default=ResourceManager.get("assistant_description.txt")
    )


class Prompt(BaseModel):
    user = peewee.ForeignKeyField(User, backref="promts")
    assistant = peewee.ForeignKeyField(Assistant, backref="requests")
    content = peewee.TextField()


class Response(BaseModel):
    prompt = peewee.ForeignKeyField(Prompt, backref="responses")
    content = peewee.TextField()


table_registry = [
    User,
    UserProfile,
    Assistant,
    Prompt,
    Response,
]
