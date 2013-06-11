class BaseStore(object):
    """
    Base class for datastore
    """
    def __init__(self):
        self.data = None

    def __get__(self, obj, obj_type):
        return self.data

    def __set__(self, obj, value):
        self.data = value

class MemoryStore(BaseStore):
    """
    Stores everything in memory only
    """
    pass

