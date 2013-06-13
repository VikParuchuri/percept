import csv

from fields.base import Dict
from utils.models import FieldModel
from conf.base import settings
from utils.input import DataFormats
from utils.models import RegistryCategories
from tests.framework import CSVInputTester
import os

class BaseInput(FieldModel):
    """
    Base for the input class
    """

    data = Dict()
    category = RegistryCategories.inputs
    namespace = settings.NAMESPACE
    input_format = "none"

    def __init__(self, **kwargs):
        super(BaseInput, self).__init__(**kwargs)

    def read_input(self, stream, **kwargs):
        """
        Reads the input in the specified format.  Overriden by specific input functions.
        """
        pass

    def get_data(self):
        """
        After data has been input, returns it
        """
        return self.data

class CSVInput(BaseInput):
    """
    Extends baseinput to read a csv file
    """
    input_format = DataFormats.csv
    tester = CSVInputTester
    test_cases = [{'stream' : os.path.abspath(os.path.join(settings.ENV_ROOT,'tests/data/csv/1.csv'))}]

    def read_input(self, stream, has_header=True):
        """
        input is any reader object that exposes the .read() interface
        for example:
        csv_input = CSVInput()
        csv_input.read_input(open("csvfile.csv"))
        """

        reader = csv.reader(stream)
        csv_data = []
        for (i, row) in enumerate(reader):
            if i==0:
                if not has_header:
                    csv_data.append([str(i) for i in xrange(0,len(row))])
            csv_data.append(row)
        self.data = csv_data




