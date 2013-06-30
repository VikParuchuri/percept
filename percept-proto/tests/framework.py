import logging
log = logging.getLogger(__name__)
from utils.registry import registry, find_in_registry
from utils.models import RegistryCategories, find_needed_formatter, find_needed_input

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

    def read_and_reformat(self, output_format, stream, stream_format):
        input_cls = find_needed_input(stream_format)
        input_inst = input_cls()
        input_inst.read_input(stream)

        formatter = find_needed_formatter(stream_format, output_format)
        formatter_inst = formatter()
        formatter_inst.read_input(input_inst.get_data(), stream_format)
        data = formatter_inst.get_data(output_format)
        return data

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
        dataformat = kwargs.get('dataformat')
        inst = self.cls()
        selected_registry = find_in_registry(category = RegistryCategories.inputs)
        selected_input_registry = [i for i in selected_registry if i.input_format==dataformat]
        if len(selected_input_registry)>0:
            input_inst = selected_input_registry[0]()
            input_inst.read_input(stream)
            inst.read_input(input_inst.get_data(), dataformat)
            for output_format in inst.output_formats:
                data = inst.get_data(output_format)
                assert data is not None

class NormalizationTester(Tester):
    test_case_format = {'stream' : basestring, 'dataformat' : basestring}

    def test(self, **kwargs):
        super(NormalizationTester, self).test(**kwargs)
        stream = open(kwargs.get('stream'))
        dataformat = kwargs.get('dataformat')
        inst = self.cls()
        output_format = inst.data_format
        data = self.read_and_reformat(output_format, stream, dataformat)

        inst.train(data.copy())
        assert len(inst.column_means)>0
        assert len(inst.column_stdevs)>0

        prediction = inst.predict(data)
        equal_cells = int(sum((prediction == inst.data).unstack()))
        cell_count = prediction.unstack().shape[0]
        assert  equal_cells == cell_count

class SVMTester(Tester):
    test_case_format = {'stream' : basestring, 'dataformat' : basestring}

    def test(self, **kwargs):
        super(SVMTester, self).test(**kwargs)
        stream = open(kwargs.get('stream'))
        dataformat = kwargs.get('dataformat')
        inst = self.cls()
        output_format = inst.data_format
        data = self.read_and_reformat(output_format, stream, dataformat)

        inst.train(data)
        assert inst.clf is not None

        prediction = inst.predict(data)
        log.info(prediction)
        raise