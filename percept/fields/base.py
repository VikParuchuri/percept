"""
Define fields for tasks and formatters
"""

import json
from percept.utils.input import import_from_string
from percept.conf.base import settings
import logging
import pickle

log = logging.getLogger(__name__)

class Field(object):
    """
    A field that is used as a descriptor on classes.
    Caches the value in one of several ways
    """
    #Type of caching is defined in settings
    value_cls = import_from_string(settings.CACHE)
    default = None

    def __init__(self, required_input = False):
        #Initialize the storage class
        self.value = self.value_cls()
        self.required_input = required_input
        if self.default is not None:
            self.__set__(None, self.default)

    def __get__(self, obj, obj_type):
        """
        As a descriptor, override __get__
        """
        #This ensures that the field is retrieved when needed
        if obj is None:
            return self
        #Whether or not to convert values to/from json
        if settings.SERIALIZE_CACHE_VALUES:
            return self.from_json(self.value)
        else:
            return self.value

    def __set__(self, obj, value):
        """
        Overrides __set__, as a descriptor
        """
        #Whether or not to convert values to/from json
        if settings.SERIALIZE_CACHE_VALUES:
            self.value = self.to_json(value)
        else:
            self.value = value

    def to_json(self, value):
        """
        Override if implementing.  Conversion to json.
        """
        return value

    def from_json(self, value):
        """
        Override if implementing.  Conversion from json.
        """
        return value

class ValueField(Field):
    """
    A basic field to store a value
    """
    def to_json(self, value):
        return json.dumps(value)

    def from_json(self, value):
        try:
            new_value = json.loads(value)
        except Exception:
            log.exception("Could not load value from json. : {0}".format(value))
            new_value = None
        return new_value

class Int(ValueField):
    """
    Store integer values
    """
    def from_json(self, value):
        try:
            new_value = int(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Boolean(ValueField):
    """
    Store boolean values
    """
    def from_json(self, value):
        try:
            new_value = bool(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Float(ValueField):
    """
    Store float values
    """
    def from_json(self, value):
        try:
            new_value = float(json.loads(value))
        except Exception:
            new_value = None
        return new_value

class Dict(ValueField):
    """
    Store dictionaries
    """
    pass

class List(ValueField):
    """
    Store lists
    """
    default = []

class String(ValueField):
    """
    Store strings
    """
    pass

class Complex(ValueField):
    """
    Store complex objects, such as classes
    """
    def to_json(self, value):
        return pickle.dumps(value)

    def from_json(self, value):
        try:
            new_value = pickle.loads(value)
        except Exception:
            log.exception("Could not unpickle value. : {0}".format(value))
            new_value = None
        return new_value
