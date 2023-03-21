import datetime as dt
from typing import Optional

from alfred.models.user import User
from alfred.frontend.functions import get_user_with_warning
from alfred.utils.string_ops import camel_to_snake


class ViewInterface:
    order_reference: int
    _instance = None

    def __init__(self):
        raise ValueError

    def __new__(cls, *args, **kwargs):
        cls.view_timestamp = dt.datetime.utcnow().isoformat()
        return super().__new__(cls)

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        return cls._instance

    @property
    def alias(self) -> str:
        return camel_to_snake(self.__name__)

    @property
    def user(self) -> Optional[User]:
        return get_user_with_warning()

    def run(self):
        raise NotImplementedError
