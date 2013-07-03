"""
Used to save and load workflows
"""

from utils.input import import_from_string
from conf.base import settings
import pickle

class BaseStore(object):
    """
    Basic datastore
    """
    def __init__(self):
        self.data_path = settings.DATA_PATH

    def save(self, obj, id_code):
        """
        Save an object, and use id_code in the filename
        obj - any object
        id_code - unique identifier
        """
        filestream = open('{0}/{1}'.format(self.data_path, id_code), 'w+')
        pickle.dump(obj, filestream)
        filestream.close()

    def load(self, id_code):
        """
        Loads a workflow identified by id_code
        id_code - unique identifier, previously must have called save with same id_code
        """
        filestream = open('{0}/{1}'.format(self.data_path, id_code), 'rb')
        workflow = pickle.load(filestream)
        return workflow

class FileStore(BaseStore):
    """
    Stores everything in pickle dumps to files
    """
    pass
