import enum

from alfred.backend.interface import TextEnum, TextEnumField

class LangField(TextEnumField):

    class Enum(TextEnum):
        ALL = "multilingual"
        EN = "english"
        ES = "spanish"

class GenderField(TextEnumField):

    class Enum(TextEnum):
        UNDEFINED = enum.auto()
        OTHER = enum.auto()
        FEMALE = enum.auto()
        MALE = enum.auto()
