from typing import Generic, Type, TypeVar, Optional

import peewee

from alfred.utils.enum_types import TextEnum
from alfred.utils.string_ops import camel_to_snake

A = TypeVar("A", bound=TextEnum)
B = TypeVar("B", bound=TextEnum)


class TextEnumField(Generic[A]):
    _enum: Optional[Type[A]] = None

    @classmethod
    def get_catalog(cls) -> Type[A]:
        if not cls._enum:
            raise NotImplementedError
        return cls._enum

    class CustomDatabaseTextEnumField(Generic[B], peewee.Field):
        catalog: Type[B]
        field_type = "text"
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

        def db_value(self, value: Optional[B]) -> Optional[str]:
            if not value:
                return None
            return self.adapt(value.name)

        def python_value(self, value: str) -> B:
            # Ignoring type since: Value of type "Optional[Type[TextEnum]]" is not indexable
            # At this point, we can guarantee that we have a Type[TextEnum]
            return self.catalog[value]  # type: ignore

    def __new__(cls, **kwargs):
        # Redirect to the inner class and define the catalog & ref attrs
        database_field_class = cls.CustomDatabaseTextEnumField
        database_field_class.catalog = cls.get_catalog()
        database_field_class.refs = camel_to_snake(cls.__name__)
        return database_field_class[A](**kwargs)
