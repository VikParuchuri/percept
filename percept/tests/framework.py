"""
Testing framework
"""

import logging
log = logging.getLogger(__name__)
from percept.utils.registry import registry, find_in_registry
from percept.utils.models import RegistryCategories, find_needed_formatter, find_needed_input
import numpy as np

class Tester(object):
    """
    Base tester class.  Testers are specified by task/workflow/formatter classes, and are used to test them.
    """
    #Defines the needed format for test cases
    test_case_format = {}
    def run(self, cls, test_cases):
        """
        Runs the tests
        """
        self.cls = cls
        for case in test_cases:
            self.test(**case)

    def test(self, **kwargs):
        """
        Specific test logic
        """
        #Look for needed arguments in test cases
        for arg in self.test_case_format.keys():
            if arg not in kwargs:
                raise Exception("Missing required key {0} in test case".format(arg))
            assert isinstance(kwargs[arg], self.test_case_format[arg])

    def read_and_reformat(self, output_format, stream, stream_format):
        """
        Reformat data according to needed formats
        """
        #Find an appropriate input class
        input_cls = find_needed_input(stream_format)
        input_inst = input_cls()
        input_inst.read_input(stream)

        #find a formatter class and convert data
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
        assert equal_cells == cell_count

class SVMTester(Tester):
    test_case_format = {'data' : basestring, 'target' : basestring, 'dataformat' : basestring}

    def test(self, **kwargs):
        super(SVMTester, self).test(**kwargs)
        datafile = open(kwargs.get('data'))
        targetfile = open(kwargs.get('target'))
        dataformat = kwargs.get('dataformat')

        inst = self.cls()
        output_format = inst.data_format
        data = self.read_and_reformat(output_format, datafile, dataformat)
        target = self.read_and_reformat(output_format, targetfile, dataformat)

        inst.train(data, target)
        assert inst.clf is not None

        prediction = inst.predict(data)
        assert isinstance(prediction, np.ndarray)

class NaiveWorkflowTester(Tester):
    test_case_format = {'config_file' : basestring}

    def test(self, **kwargs):
        super(NaiveWorkflowTester, self).test(**kwargs)
        config_file = kwargs.get('config_file')

        from percept.utils.workflow import WorkflowWrapper
        wrapper = WorkflowWrapper(config_file, self.cls)
        wrapper.run()

        assert wrapper.workflow.setup_run == True
