import enum

from alfred.utils.enum_types import TextEnum


class Status(TextEnum):
    SUCCESS = enum.auto()
    FAILURE = enum.auto()

    @classmethod
    def from_bool(cls, ok: bool) -> 'Status':
        return cls.SUCCESS if ok else cls.FAILURE
