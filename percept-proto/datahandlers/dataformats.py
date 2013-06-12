from pandas import DataFrame
import numpy as np
from utils.models import FieldModel

from fields.base import Dict
from conf.base import settings
from utils.models import RegistryCategories
import re

class DataFormats(object):
    csv = "csv"
    dataframe = "dataframe"


class BaseFormat(FieldModel):
    """
    Base class to reformat input data
    """
    data = Dict()
    category = RegistryCategories.dataformats
    namespace = settings.NAMESPACE

    def __init__(self, input_data, data_format, **kwargs):
        super(BaseFormat, self).__init__(**kwargs)
        self.input_data = input_data
        self.data_format = data_format
        self.input_formats = []
        self.output_formats = []
        self.setup_formats()

    def setup_formats(self):
        methods = self.get_methods()
        for m in methods:
            if m.startswith("from_"):
                self.input_formats.append(re.sub("from_" , "",m))
            elif m.startswith("to_"):
                self.output_formats.append(re.sub("to_","",m))

    def read_input(self):
        data_converter = getattr(self, "from_" + self.data_format)
        self.data = data_converter(self.input_data)

    def get_data(self, data_format):
        data_converter = getattr(self, "to_" + data_format)
        return data_converter(self.data)

class JSONFormat(BaseFormat):
    """
    Converts everything to a base json format, and then converts from that format to output formats, like a pandas dataframe
    """
    input_formats = [DataFormats.csv]
    output_formats = [DataFormats.dataframe]
    def from_csv(self):
        reformatted_data = []
        for (i,row) in enumerate(self.input_data):
            if i==0:
                headers = row
            else:
                data_row = {}
                for (j,h) in enumerate(headers):
                    data_row.update({h : row[j]})
                reformatted_data.append(data_row)
        return reformatted_data

    def to_dataframe(self):
        keys = self.data[0].keys()
        column_list =[]
        for k in keys:
            key_list = []
            for i in xrange(0,len(self.data)):
                key_list.append(self.data[i][k])
            column_list.append(key_list)
        return DataFrame(np.asarray(column_list), columns=keys)





