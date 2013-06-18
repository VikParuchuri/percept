executed_functions = []

class BaseStore(object):
    """
    Base class for datastore
    """
    def __init__(self):
        self.data = None

    def retrieve(self, obj, args, run_id):
        if obj is None:
            return self
        return self.data

    def store(self, obj, args, run_id):
        self.data = value

    def generate_identifier(self, obj, run_id):
        identifier = "{0}-{1}-{2}-{3}".format(obj.category, obj.namespace, obj.name, run_id)
        return identifier


class MemoryStore(BaseStore):
    """
    Stores everything in memory only
    """
    pass
