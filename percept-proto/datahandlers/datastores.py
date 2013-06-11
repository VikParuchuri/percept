class BaseStore(object):
    """
    Base class for datastore
    """
    def __init__(self, data):
        self.data = data

    def get_data_iter(self):
        i = 0
        while i < self.data.rows:
            yield self.data[i]
            i +=1

    def get_all_data(self):
        return self.data

class MemoryStore(BaseStore):
    """
    Stores everything in memory only
    """
    pass

