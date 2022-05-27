import json

from django.db import models
from django.utils.translation import gettext_lazy as _


class SubList(list):
    def __init__(self, delimiter, *args):
        self.delimiter = delimiter
        super().__init__(*args)

    def __str__(self):
        return self.delimiter.join(self)


class ListField(models.TextField):
    """
    Special Field type specially design to work with Lists for special databases
    """
    description = _("Group Concat List field")

    def __init__(self, *args, **kwargs):
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(*args, **kwargs)

    def parse(self, value_string):
        json_value = json.loads(value_string)
        return list(json_value)

    def get_internal_type(self):
        return "ListField"

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.delimiter)
        return SubList(self.delimiter, value.split(self.delimiter))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
