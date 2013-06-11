from pandas import DataFrame
import numpy as np

class DataFormats(object):
    csv = "csv"
    dataframe = "dataframe"


class BaseFormat(object):
    """
    Base class to reformat input data
    """
    def __init__(self, data, data_format):
        self.input_data = data
        self.input_format = data_format
        self.data = None

    def read_input(self):
        data_converter = getattr(self, "from_" + self.input_format)
        self.data = data_converter(self.input_data)

    def get_data(self, data_format):
        data_converter = getattr(self, "to_" + data_format)
        return data_converter(self.data)

class JSONFormat(BaseFormat):
    """
    Converts everything to a base json format, and then converts from that format to output formats, like a pandas dataframe
    """
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





