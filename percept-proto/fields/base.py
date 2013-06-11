import json
from utils.input import import_from_string
from conf.base import settings

class Field(object):
    value = import_from_string(settings.DATASTORE)()
    def __init__(self, required_input = False):
        self.required_input = required_input

    def __get__(self, obj, obj_type):
        return self.from_json(self.value)

    def __set__(self, obj, value):
        self.value = self.to_json(value)

    def to_json(self, value):
        return value

    def from_json(self, value):
        return value

class ValueField(Field):
    def to_json(self, value):
        return json.dumps(value)

    def from_json(self, value):
        try:
            new_value = json.loads(value)
        except Exception:
            new_value = None
        return new_value

class Int(ValueField):
    def from_json(self, value):
        try:
            new_value = int(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Boolean(ValueField):
    def from_json(self, value):
        try:
            new_value = bool(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Float(ValueField):
    def from_json(self, value):
        try:
            new_value = float(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Dict(ValueField):
    pass

class List(ValueField):
    pass

class String(ValueField):
    pass
