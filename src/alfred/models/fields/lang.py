from alfred.models.enums import Lang
from alfred.dao.field_types import TextEnumField


class LangField(TextEnumField[Lang]):
    _enum = Lang
