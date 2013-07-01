from utils.input import import_from_string
from conf.base import settings
import pickle

class WorkflowLoader(object):
    """
    Loads and saves workflows
    """
    store = import_from_string(settings.DATASTORE)

    def __init__(self):
        self.store = self.store()

    def load(self, cls, run_id):
        id_code = self.generate_load_identifier(cls, run_id)
        inst = self.store.load(id_code)
        return inst

    def save(self, obj, run_id):
        id_code = self.generate_save_identifier(obj, run_id)
        inst = self.store.save(id_code)

    def _save(self, obj, id_code):

    def generate_save_identifier(self, obj, run_id):
        identifier = "{0}-{1}".format(obj.__class__.lower(), run_id)
        return identifier

    def generate_load_identifier(self, cls, run_id):
        identifier = "{0}.{1}-{2}".format(cls.__module__.lower(), cls.__name__.lower(), run_id)
        return identifier

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
