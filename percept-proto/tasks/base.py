from fields.base import Dict, List, Int, Boolean, String

class Task(object):
    input_values = []
    stored_values = []
    def __init__(self, **kwargs):
        for key in self.input_values:
            if key not in kwargs:
                raise Exception("Required key {0} not found in inputs.".format(key))

        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def train(self):
        pass

    def predict(self):
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
