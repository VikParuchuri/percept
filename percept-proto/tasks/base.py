from fields.base import Dict, List, Int, Boolean, String
import inspect
import logging

log = logging.getLogger(__name__)

class Task(object):
    data = Dict()
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

    def train(self):
        pass

    def predict(self):
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
