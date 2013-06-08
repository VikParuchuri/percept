class BaseStore(object):
    """
    Base class for dataformat
    """
    def __init__(self, data):
        self.reformat_data(data)

    def reformat_data(self, data):
        pass

    def get_data_iter(self):
        i = 0
        while i < self.data.rows:
            yield self.data[i]
            i +=1

    def get_all_data(self):
        return self.data

class MemoryStore(BaseStore):
    pass

