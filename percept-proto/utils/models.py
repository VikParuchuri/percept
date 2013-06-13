import inspect
from conf.base import settings
import logging
from collections import namedtuple
import inspect

log = logging.getLogger(__name__)

def find_needed_formatter(input_format, output_format):
    selected_registry = [re.cls for re in registry if re.category==RegistryCategories.formatters]
    needed_formatters = []
    for formatter in selected_registry:
        formatter_inst = formatter()
        if input_format in formatter_inst.input_formats and output_format in formatter_inst.output_formats:
            needed_formatters.append(formatter)
    if len(needed_formatters)>0:
        return needed_formatters[0]
    return None

def exists_in_registry(category, namespace, name):
    selected_registry = [re for re in registry if re.category==category and re.namespace==namespace and re.name == name]
    if len(selected_registry)>0:
        return True
    return False

class RegistryCategories(object):
    base = "base"
    preprocessors = "preprocessors"
    inputs = "inputs"
    formatters = "formatters"

RegistryEntry = namedtuple('RegistryEntry', ['category', 'namespace', 'name', 'cls'], verbose=True)

registry = []

def register(cls):
    registry_entry = RegistryEntry(category = cls.category, namespace = cls.namespace, name = cls.name, cls=cls)
    if registry_entry not in registry and not exists_in_registry(cls.category, cls.namespace, cls.name):
        registry.append(registry_entry)
    else:
        log.warn("Class {0} already in registry".format(cls))

class MetaFieldModel(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, MetaFieldModel).__new__(cls, clsname, bases, attrs)
        newclass.name = newclass.__name__.lower()
        register(newclass)
        return newclass

class FieldModel(object):
    __metaclass__ = MetaFieldModel
    category = RegistryCategories.base
    namespace = settings.NAMESPACE
    name = __name__.lower()

    def __init__(self, **kwargs):
        self._set_fields()
        for key in self.required_input:
            if key not in kwargs:
                raise Exception("Required key {0} not found in inputs.".format(key))

        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def _set_fields(self):
        self.fields = []
        self.required_input = []
        for member_name, member_object in inspect.getmembers(self.__class__):
            if inspect.isdatadescriptor(member_object) and not member_name.startswith("__"):
                self.fields.append(member_name)
                if member_object.required_input:
                    self.required_input.append(member_name)

    def get_data(self):
        data_dict = {}
        for key in self.fields:
            data_dict.update({key : getattr(self,key)})
        return data_dict

    def get_methods(self):
        method_tuples = inspect.getmembers(self.__class__)
        methods = []
        for m,s in method_tuples:
            if not m.startswith("__"):
                methods.append(m)
        return methods

