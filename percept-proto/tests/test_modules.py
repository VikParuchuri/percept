import os
ROOT_PATH = os.path.abspath(__file__)
TEST_PATH = os.path.abspath(os.path.join(ROOT_PATH, ".."))
TEST_DATA_PATH = os.path.abspath(os.path.join(TEST_PATH, "data"))

os.environ["PERCEPT_SETTINGS_MODULE"] = "percept-proto.tests.test_settings"

from conf.base import settings
from utils.models import find_in_registry, RegistryCategories, registry
from fields.base import Dict
import unittest
import logging

log = logging.getLogger(__name__)

class GenericTest(object):
    name = ""
    category = ""
    namespace = ""

    def generic_setup(self):
        self.cls = find_in_registry(category=self.category, namespace = self.namespace, name = self.name)
        if self.cls is None:
            raise Exception("Cannot find a module with category {0}, namespace {1}, and name {2}".format(self.category, self.namespace, self.name))

class DataLoader(object):
    def __init__(self, dataformat):
        datapath = os.path.abspath(os.path.join(TEST_DATA_PATH, dataformat))
        filenames = os.listdir(datapath)
        self.filenames = [os.path.abspath(os.path.join(datapath,f)) for f in filenames if os.path.isfile(os.path.join(datapath,f))]

    def get_streams(self):
        stream_list = []
        for f in self.filenames:
            stream_list.append(open(f))
        return stream_list

class InputTest(unittest.TestCase, GenericTest):
    category = RegistryCategories.inputs
    namespace = settings.NAMESPACE

    def setUp(self):
        log.info(registry)
        self.generic_setup()

    def test_read(self):
        for cls in self.cls:
            dataformat = cls.input_format
            dataloader = DataLoader(dataformat)
            datastreams = dataloader.get_streams()
            for stream in datastreams:
                obj = cls(stream)
                assert isinstance(obj.data, Dict)




