"""
Testing framework
"""

import logging
log = logging.getLogger(__name__)
from percept.utils.models import RegistryCategories, find_needed_formatter, find_needed_input
import numpy as np
from pandas import read_csv

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

class NormalizationTester(Tester):
    test_case_format = {'stream' : basestring}

    def test(self, **kwargs):
        super(NormalizationTester, self).test(**kwargs)
        stream = kwargs.get('stream')
        inst = self.cls()
        data = read_csv(stream)

        inst.train(data.copy())
        assert len(inst.column_means)>0
        assert len(inst.column_stdevs)>0

        prediction = inst.predict(data)
        equal_cells = int(sum((prediction == inst.data).unstack()))
        cell_count = prediction.unstack().shape[0]
        assert equal_cells == cell_count

class SVMTester(Tester):
    test_case_format = {'data' : basestring, 'target' : basestring}

    def test(self, **kwargs):
        super(SVMTester, self).test(**kwargs)
        datafile = kwargs.get('data')
        targetfile = kwargs.get('target')

        inst = self.cls()
        data = read_csv(datafile)
        target = read_csv(targetfile)

        inst.train(data,target=target)
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