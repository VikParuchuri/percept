from fields.base import Dict, List, Int, Boolean, String
from utils.models import FieldModel
from datahandlers.dataformats import DataFormats
import logging

log = logging.getLogger(__name__)

class Task(FieldModel):
    data = Dict()
    data_format = String(value=DataFormats.dataframe)
    def __init__(self, **kwargs):
        super(Task,self).__init__(**kwargs)

    def convert_to_format(self):


    def train(self, **kwargs):
        pass

    def predict(self, test_data, **kwargs):
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
