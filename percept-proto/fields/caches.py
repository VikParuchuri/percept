"""
Data caching, used by fields.base
"""

class BaseCache(object):
    """
    Base class for datastore.  Used by fields.base to cache.
    """
    def __init__(self):
        self.data = None

    def __get__(self, obj, obj_type):
        if obj is None:
            return self
        return self.data

    def __set__(self, obj, value):
        self.data = value

class MemoryCache(BaseCache):
    """
    Stores everything in memory only
    """
    pass

