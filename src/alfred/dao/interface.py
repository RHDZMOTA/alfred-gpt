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

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name.lower()


class TextEnumField:

    @classmethod
    def get_catalog(cls) -> Type[TextEnum]:
        return getattr(cls, "Enum") or (
            lambda: (_ for _ in ()).throw(NotImplementedError)
        )()

    class CustomDatabaseTextEnumField(peewee.Field):
        field_type = "text"
        catalog: Optional[Type[TextEnum]] = None
        refs: Optional[str] = None

        def __init__(self, **kwargs):
            # The catalog should be implemented before creating an instance
            if self.catalog is None:
                raise NotImplementedError
            # Define default kwargs: choices, help_text
            # These values can be overwritten if the arguments are provided
            kwargs = {
                "choices": [
                    (enum, enum.value)
                    for enum in self.catalog
                ],
                "help_text": f"This is an enum text field: {self.refs}",
                **kwargs
            }
            super().__init__(**kwargs)

        def db_value(self, value: Optional[Type[TextEnum]]) -> Optional[str]:
            if not value:
                return None
            return super().adapt(value.name)

        def python_value(self, value: str) -> TextEnum:
            # Ignoring type since: Value of type "Optional[Type[TextEnum]]" is not indexable
            # At this point, we can guarantee that we have a Type[TextEnum]
            return self.catalog[value]  # type: ignore

    def __new__(cls, **kwargs):
        # Redirect to the inner class and define the catalog & ref attrs
        database_field_class = cls.CustomDatabaseTextEnumField
        database_field_class.catalog = cls.get_catalog()
        database_field_class.refs = camel_to_snake(cls.__name__)
        return database_field_class(**kwargs)
