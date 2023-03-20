
from alfred.models.enums import Gender
from alfred.dao.field_types import TextEnumField


class GenderField(TextEnumField[Gender]):
    _enum = Gender
