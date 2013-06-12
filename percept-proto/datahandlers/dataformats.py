from pandas import DataFrame
import numpy as np
from utils.models import FieldModel

from fields.base import Dict
from conf.base import settings
from utils.models import RegistryCategories
import re
import logging
log = logging.getLogger(__name__)

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

    def __init__(self, **kwargs):
        super(BaseFormat, self).__init__(**kwargs)
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

    def read_input(self, input_data, data_format):
        if data_format not in self.input_formats:
            raise Exception("Input format {0} not available with this class. Available formats are {1}.".format(data_format, self.input_formats))
        data_converter = getattr(self, "from_" + data_format)
        self.data = data_converter(input_data)

    def get_data(self, data_format):
        if data_format not in self.output_formats:
            raise Exception("Output format {0} not available with this class. Available formats are {1}.".format(data_format, self.output_formats))
        data_converter = getattr(self, "to_" + data_format)
        return data_converter()

class JSONFormat(BaseFormat):
    """
    Converts everything to a base json format, and then converts from that format to output formats, like a pandas dataframe
    """
    def from_csv(self, input_data):
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
        keys = self.data[0].keys()
        column_list =[]
        for k in keys:
            key_list = []
            for i in xrange(0,len(self.data)):
                key_list.append(self.data[i][k])
            column_list.append(key_list)
        log.info(column_list)
        log.info(keys)
        log.info(np.asarray(column_list))
        return DataFrame(np.asarray(column_list), columns=keys)





