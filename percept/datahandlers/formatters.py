"""
Data formatters.  Will take data from many formats, pass through a common format, and output to many formats.
"""

from pandas import DataFrame
import numpy as np
from percept.utils.models import FieldModel

from percept.fields.base import Dict
from percept.conf.base import settings
from percept.utils.models import RegistryCategories
from percept.utils.input import DataFormats
from percept.tests.framework import JSONFormatTester
import os
import re
import logging
log = logging.getLogger(__name__)

class BaseFormat(FieldModel):
    """
    Base class to reformat input data.  If implementing, add in from_ and to_ methods (see read_input and get_data)
    """
    #These fields will be cached.  See fields.base
    data = Dict()

    #Set the category and namespace for the registry
    category = RegistryCategories.formatters
    namespace = settings.NAMESPACE

    help_text = "Base class for reformatting input data.  Do not use directly."

    def __init__(self, **kwargs):
        super(BaseFormat, self).__init__(**kwargs)
        self.input_formats = []
        self.output_formats = []
        self.setup_formats()

    def setup_formats(self):
        """
        Inspects its methods to see what it can convert from and to
        """
        methods = self.get_methods()
        for m in methods:
            #Methods named "from_X" will be assumed to convert from format X to the common format
            if m.startswith("from_"):
                self.input_formats.append(re.sub("from_" , "",m))
            #Methods named "to_X" will be assumed to convert from the common format to X
            elif m.startswith("to_"):
                self.output_formats.append(re.sub("to_","",m))

    def read_input(self, input_data, data_format):
        """
        Reads the input data and converts to common format
        input_data - the output from one of the input classes (ie CSVInput)
        data_format - the format of the data.  See utils.input.dataformats
        """
        if data_format not in self.input_formats:
            raise Exception("Input format {0} not available with this class. Available formats are {1}.".format(data_format, self.input_formats))
        data_converter = getattr(self, "from_" + data_format)
        self.data = data_converter(input_data)

    def get_data(self, data_format):
        """
        Reads the common format and converts to output data
        data_format - the format of the output data.  See utils.input.dataformats
        """
        if data_format not in self.output_formats:
            raise Exception("Output format {0} not available with this class. Available formats are {1}.".format(data_format, self.output_formats))
        data_converter = getattr(self, "to_" + data_format)
        return data_converter()

class JSONFormat(BaseFormat):
    """
    Converts everything to a base json format, and then converts from that format to output formats, like a pandas dataframe.
    There are ways to convert directly from csv to a dataframe, but this is an example class.
    """
    #Tester and test_cases are used by the testing framework.  See tests.framework
    tester = JSONFormatTester
    test_cases = [{'stream' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1/data.csv')), 'dataformat' : DataFormats.csv}]

    help_text = "Example class to convert from csv to dataframe."

    def from_csv(self, input_data):
        """
        Reads csv format input data and converts to json.
        """
        reformatted_data = []
        for (i,row) in enumerate(input_data):
            if i==0:
                headers = row
            else:
                data_row = {}
                for (j,h) in enumerate(headers):
                    data_row.update({h : row[j]})
                reformatted_data.append(data_row)
        return reformatted_data

    def to_dataframe(self):
        """
        Reads the common format self.data and writes out to a dataframe.
        """
        keys = self.data[0].keys()
        column_list =[]
        for k in keys:
            key_list = []
            for i in xrange(0,len(self.data)):
                key_list.append(self.data[i][k])
            column_list.append(key_list)
        df = DataFrame(np.asarray(column_list).transpose(), columns=keys)
        for i in xrange(0,df.shape[0]):
            df.iloc[i] = df.iloc[i].astype(float)
        return df





