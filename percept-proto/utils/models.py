import inspect
from collections import namedtuple

RegistryEntry = namedtuple('RegistryEntry', ['category', 'namespace', 'name', 'cls'], verbose=True)

registry = []

def register(cls):
    registry_entry = RegistryEntry(category = cls.category, namespace = cls.namespace, name = cls.name, cls=cls)
    if registry_entry not in registry:
        registry.append(registry_entry)

class MetaFieldModel(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, MetaFieldModel).__new__(cls, clsname, bases, attrs)
        register(newclass)
        return newclass

class FieldModel(object):
    __metaclass__ = MetaFieldModel
    category = "base"
    namespace = "percept"
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
