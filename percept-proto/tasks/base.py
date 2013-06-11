from fields.base import Dict, List, Int, Boolean, String
from utils.models import FieldModel
import logging

log = logging.getLogger(__name__)

class Task(FieldModel):
    data = Dict()
    def __init__(self, **kwargs):
        super(Task,self).__init__(**kwargs)

    def train(self):
        pass

    def predict(self):
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
