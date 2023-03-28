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
        name = getattr(self, "__name__")  # Why not self.__name__? Because mypy...
        # References:
        # - https://github.com/python/cpython/issues/88690
        # - https://github.com/python/mypy/issues/10403
        # - https://github.com/python/mypy/issues/12795
        # - https://docs.python.org/3/library/stdtypes.html#definition.__name__
        return camel_to_snake(name)

    @property
    def user(self) -> Optional[User]:
        return get_user_with_warning()

    def run(self):
        raise NotImplementedError
