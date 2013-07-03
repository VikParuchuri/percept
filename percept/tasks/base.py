"""
Tasks are run on data, and can include transforms and algorithms
"""

from percept.fields.base import Dict, List, Int, Boolean, String
from percept.utils.models import FieldModel
from percept.utils.input import DataFormats
from percept.conf.base import settings
from percept.utils.models import RegistryCategories
from collections import namedtuple

import logging
log = logging.getLogger(__name__)

Dependency = namedtuple("Dependency", ['cls', 'args'], verbose=False)

class Task(FieldModel):
    """
    Base class for task
    """
    #Used by the registry
    category = RegistryCategories.base
    namespace = settings.NAMESPACE

    #Define dependencies to run before this (results are passed into class before execution)
    dependencies = []
    trained_dependencies = []

    #Additional arguments to pass into train and predict functions (additional data files, etc)
    args = {}

    #Data format accepted
    data_format = DataFormats.dataframe

    #Cached field
    data = Dict()

    help_text = "Base task class. Do not use directly."

    def __init__(self, **kwargs):
        super(Task,self).__init__(**kwargs)

    def train(self, data, **kwargs):
        """
        Used in the training phase.  Override.
        """
        pass

    def predict(self, test_data, **kwargs):
        """
        Used in the predict phase, after training.  Override
        """
        pass

    def get_data(self):
        data_dict = {}
        for key in self.stored_values:
            data_dict.update({key : getattr(self,key)})
