from utils.input import import_from_string
from conf.base import settings
import pickle

class BaseStore(object):
    def __init__(self):
        self.data_path = settings.DATA_PATH

    def save(self, obj, id_code):
        filestream = open('{0}/{1}'.format(self.data_path, id_code), 'w+')
        pickle.dump(obj, filestream)
        filestream.close()

    def load(self, id_code):
        filestream = open('{0}/{1}'.format(self.data_path, id_code), 'rb')
        workflow = pickle.load(filestream)
        return workflow

class FileStore(BaseStore):
    """
    Stores everything in pickle dumps to files
    """
    pass
