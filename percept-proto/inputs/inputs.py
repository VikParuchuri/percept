import csv

class BaseInput(object):
    """
    Base for the input class
    """

    def __init__(self, stream):
        self.stream = stream
        self.data = None

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




