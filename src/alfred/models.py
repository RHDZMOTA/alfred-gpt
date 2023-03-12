import enum


class Status(enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"

    @classmethod
    def from_bool(cls, ok: bool) -> 'Status':
        return cls.SUCCESS if ok else cls.FAILURE
