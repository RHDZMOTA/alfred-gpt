import peewee

from alfred.dao.interface import BaseModel
from alfred.settings import (
    ALFRED_ACTIVATION_CODES,
    get_logger,
)
from alfred.utils.pwd import password_cooking


logger = get_logger(name=__name__)


class User(BaseModel):
    name = peewee.CharField(
        null=False,
        unique=True,
    )
    email = peewee.CharField(
        null=False,
        unique=True,
    )
    password_hash = peewee.CharField(
        null=False,
    )
    password_salt = peewee.CharField(
        null=False,
    )
    verified = peewee.BooleanField(
        default=False,
        null=False,
    )

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
