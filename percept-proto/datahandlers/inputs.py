import csv

from fields.base import Dict
from utils.models import FieldModel
from conf.base import settings
from utils.models import RegistryCategories, DataFormats

class BaseInput(FieldModel):
    """
    Base for the input class
    """

    data = Dict()
    category = RegistryCategories.inputs
    namespace = settings.NAMESPACE
    input_format = ""

    def __init__(self, stream, **kwargs):
        super(BaseInput, self).__init__(**kwargs)
        self.stream = stream

    def read_input(self):
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

    def read_input(self, has_header=True):
        """
        input is any reader object that exposes the .read() interface
        for example:
        csv_input = CSVInput()
        csv_input.read_input(open("csvfile.csv"))
        """

        reader = csv.reader(self.stream)
        csv_data = []
        for (i, row) in enumerate(reader):
            if i==0:
                if not has_header():
                    csv_data.append([str(i) for i in xrange(0,len(row))])
            csv_data.append(row)
        self.data = csv_data




