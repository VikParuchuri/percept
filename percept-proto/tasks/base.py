from fields.base import Dict, List, Int, Boolean, String
from utils.models import FieldModel
from utils.input import DataFormats
from conf.base import settings
from utils.models import RegistryCategories
from collections import namedtuple

import logging
log = logging.getLogger(__name__)

Dependency = namedtuple("Dependency", ['cls', 'args'], verbose=False)

class Task(FieldModel):
    category = RegistryCategories.base
    namespace = settings.NAMESPACE
    dependencies = []
    trained_dependencies = []
    args = {}
    data_format = DataFormats.dataframe
    data = Dict()

    def __init__(self, **kwargs):
        super(Task,self).__init__(**kwargs)

    def train(self, data, **kwargs):
        pass

    def predict(self, test_data, **kwargs):
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
