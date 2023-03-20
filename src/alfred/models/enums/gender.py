import enum

from alfred.utils.enum_types import TextEnum


class Gender(TextEnum):
    UNDEFINED = enum.auto()
    OTHER = enum.auto()
    FEMALE = enum.auto()
    MALE = enum.auto()
