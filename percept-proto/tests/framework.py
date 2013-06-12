import logging
log = logging.getLogger(__name__)
from utils.registry import registry, find_in_registry
from utils.models import RegistryCategories

class Tester(object):
    test_case_format = {}
    def run(self, cls, test_cases):
        self.cls = cls
        for case in test_cases:
            self.test(**case)

    def test(self, **kwargs):
        for arg in self.test_case_format.keys():
            if arg not in kwargs:
                raise Exception("Missing required key {0} in test case".format(arg))
            assert isinstance(kwargs[arg], self.test_case_format[arg])

class CSVInputTester(Tester):
    test_case_format = {'stream' : basestring}

    def test(self, **kwargs):
        super(CSVInputTester, self).test(**kwargs)
        stream = open(kwargs.get('stream'))
        inst = self.cls()
        inst.read_input(stream)
        assert isinstance(inst.data, list)

class JSONFormatTester(Tester):
    test_case_format = {'stream' : basestring, 'dataformat' : basestring}

    def test(self, **kwargs):
        super(JSONFormatTester, self).test(**kwargs)
        stream = open(kwargs.get('stream'))
        dataformat = kwargs.get('format')
        inst = self.cls()
        selected_registry = find_in_registry(category = RegistryCategories.inputs)
        selected_input_registry = [i for i in selected_registry if i.input_format==dataformat]
        if len(selected_input_registry)>0:
            input_inst = selected_input_registry[0]()
            input_inst.read_input(stream)
            inst.read_input(input_inst.data, dataformat)
            for output_format in inst.output_formats:
                data = inst.get_data(output_format)
                assert isinstance(data, list)