import enum
from typing import Any, Type, Optional

import peewee

from alfred.utils import camel_to_snake

# Inspired on:
# - https://github.com/python/cpython/blob/4d1f033986675b883b9ff14588ae6ff78fdde313/Lib/enum.py#L1265
# - https://docs.python.org/3.11/library/enum.html#enum.StrEnum
class TextEnum(str, enum.Enum):
    
    def __new__(cls, value: str):
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name.lower()

