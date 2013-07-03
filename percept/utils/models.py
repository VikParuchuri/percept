"""
Model and registry utility functions
"""

import inspect
from conf.base import settings
import logging
from collections import namedtuple
import inspect

log = logging.getLogger(__name__)

def get_task_name(obj):
    try:
        name = "{0}.{1}.{2}".format(obj.category, obj.namespace, obj.name)
    except AttributeError:
        name = obj.__class__.__name__

    return name

def find_needed_formatter(input_format, output_format):
    """
    Find a data formatter given an input and output format
    input_format - needed input format.  see utils.input.dataformats
    output_format - needed output format.  see utils.input.dataformats
    """
    #Only take the formatters in the registry
    selected_registry = [re.cls for re in registry if re.category==RegistryCategories.formatters]
    needed_formatters = []
    for formatter in selected_registry:
        #Initialize the formatter (needed so it can discover its formats)
        formatter_inst = formatter()
        if input_format in formatter_inst.input_formats and output_format in formatter_inst.output_formats:
            needed_formatters.append(formatter)
    if len(needed_formatters)>0:
        return needed_formatters[0]
    return None

def find_needed_input(input_format):
    """
    Find a needed input class
    input_format - needed input format, see utils.input.dataformats
    """
    needed_inputs = [re.cls for re in registry if re.category==RegistryCategories.inputs and re.cls.input_format == input_format]
    if len(needed_inputs)>0:
        return needed_inputs[0]
    return None

def exists_in_registry(category, namespace, name):
    """
    See if a given category, namespace, name combination exists in the registry
    category - See registrycategories.  Type of module
    namespace - Namespace of the module, defined in settings
    name - the lowercase name of the module
    """
    selected_registry = [re for re in registry if re.category==category and re.namespace==namespace and re.name == name]
    if len(selected_registry)>0:
        return True
    return False

class RegistryCategories(object):
    """
    Define valid registry categories
    """
    base = "base"
    preprocessors = "preprocessors"
    inputs = "inputs"
    formatters = "formatters"
    algorithms = "algorithms"
    workflows = "workflows"

#Each entry in the registry is a tuple
RegistryEntry = namedtuple('RegistryEntry', ['category', 'namespace', 'name', 'cls'], verbose=False)

#Registry, a list of tuples.  Defined here, but initialized in utils.registry
registry = []

def register(cls):
    """
    Register a given model in the registry
    """
    registry_entry = RegistryEntry(category = cls.category, namespace = cls.namespace, name = cls.name, cls=cls)
    if registry_entry not in registry and not exists_in_registry(cls.category, cls.namespace, cls.name):
        registry.append(registry_entry)
    else:
        log.warn("Class {0} already in registry".format(cls))

class MetaFieldModel(type):
    """
    Metaclass to facilitate registration of modules
    """
    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, MetaFieldModel).__new__(cls, clsname, bases, attrs)
        newclass.name = newclass.__name__.lower()
        register(newclass)
        return newclass

class FieldModel(object):
    """
    Base model for tasks, contains useful functions
    """
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
        """
        Initialize the fields for data caching.
        """
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

