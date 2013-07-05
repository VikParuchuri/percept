"""
Data inputs.  Take in data, and do any cleanup needed for the formatters to work.
"""

import csv

from percept.fields.base import Dict
from percept.utils.models import FieldModel
from percept.conf.base import settings
from percept.utils.input import DataFormats
from percept.utils.models import RegistryCategories, get_namespace
from percept.tests.framework import CSVInputTester
import os

class BaseInput(FieldModel):
    """
    Base for the input class
    """
    #Cached fields.  See fields.base
    data = Dict()

    #Used for the registry
    category = RegistryCategories.inputs
    namespace = get_namespace(__module__)

    input_format = "none"

    help_text = "Base class for input.  Do not use directly."

    def __init__(self, **kwargs):
        super(BaseInput, self).__init__(**kwargs)

    def read_input(self, stream, **kwargs):
        """
        Reads the input in the specified format.  Overriden by specific input functions.
        """
        pass

    def get_data(self):
        """
        After data has been input, returns it.  Override if needed.
        """
        return self.data

class CSVInput(BaseInput):
    """
    Extends baseinput to read a csv file
    """
    input_format = DataFormats.csv
    tester = CSVInputTester
    test_cases = [{'stream' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1/data.csv'))}]

    help_text = "Example class to load in csv files."

    def read_input(self, filename, has_header=True):
        """
        filename is any filename, or something on which open() can be called
        for example:
        csv_input = CSVInput()
        csv_input.read_input("csvfile.csv")
        """
        stream = open(filename)
        reader = csv.reader(stream)
        csv_data = []
        for (i, row) in enumerate(reader):
            if i==0:
                if not has_header:
                    csv_data.append([str(i) for i in xrange(0,len(row))])
            csv_data.append(row)
        self.data = csv_data




