import os
ROOT_PATH = os.path.abspath(__file__)
TEST_PATH = os.path.abspath(os.path.join(ROOT_PATH, ".."))
TEST_DATA_PATH = os.path.abspath(os.path.join(TEST_PATH, "data"))

os.environ["PERCEPT_SETTINGS_MODULE"] = "percept-proto.tests.test_settings"

from conf.base import settings
from utils.models import RegistryCategories
from utils.registry import find_in_registry, registry
import fields.base
import unittest
import logging

log = logging.getLogger(__name__)

class GenericTest(object):
    name = None
    category = None
    namespace = None

    def generic_setup(self):
        self.cls = find_in_registry(category=self.category, namespace = self.namespace, name = self.name)
        if self.cls is None:
            raise Exception("Cannot find a module with category {0}, namespace {1}, and name {2}".format(self.category, self.namespace, self.name))

class DataLoader(object):
    def __init__(self, dataformat):
        self.filenames = []
        datapath = os.path.abspath(os.path.join(TEST_DATA_PATH, dataformat))
        if os.path.isdir(datapath):
            filenames = os.listdir(datapath)
            self.filenames = [os.path.abspath(os.path.join(datapath,f)) for f in filenames if os.path.isfile(os.path.join(datapath,f))]

    def get_streams(self):
        stream_list = []
        for f in self.filenames:
            stream_list.append(open(f))
        return stream_list

def create_input(cls):
    obj_list = []
    dataformat = cls.input_format
    dataloader = DataLoader(dataformat)
    datastreams = dataloader.get_streams()
    for stream in datastreams:
        obj = cls(stream)
        obj.read_input()
        obj_list.append(obj)
    return obj_list

class InputTest(GenericTest):
    category = RegistryCategories.inputs
    namespace = settings.NAMESPACE

    def setUp(self):
        self.generic_setup()

    def test_read(self):
        for cls in self.cls:
                obj_list = create_input(cls)
                for obj in obj_list:
                    yield isinstance(obj.data, list)

def test_input():
    input_test = InputTest()
    input_test.setUp()
    input_test.test_read()

class FormatTest(unittest.TestCase, GenericTest):
    category = RegistryCategories.dataformats
    namespace = settings.NAMESPACE

    def setUp(self):
        self.generic_setup()

    def test_read(self):
        input_test = InputTest()
        for cls in input_test.cls:
            obj_list = create_input(cls)





