class DataFormats(object):
    csv = "csv"
    dataframe = "dataframe"


class BaseFormat(object):
    def __init__(self, data, data_format):
        self.input_data = data
        self.input_format = data_format
        self.data = None

    def read_input(self):
        data_converter = getattr(self, "from_" + self.input_format)
        self.data = data_converter(self.input_data)

    def from_csv(data):
        pass

    def get_data(self, data_format):
        data_converter = getattr(self, "to_" + data_format)
        return data_converter(self.data)

class JSONFormat(BaseFormat):
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
        pass




