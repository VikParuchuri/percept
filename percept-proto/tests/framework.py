import logging
log = logging.getLogger(__name__)

class Tester(object):
    test_case_format = {}
    def run(self, cls, test_cases):
        self.cls = cls
        for case in test_cases:
            self.test(**case)

    def test(self, **kwargs):
        pass

class CSVInputTester(Tester):
    test_case_format = {'stream' : basestring}

    def test(self, **kwargs):
        for arg in self.test_case_format.keys():
            if arg not in kwargs:
                raise Exception("Missing required key {0} in test case".format(arg))
            assert isinstance(kwargs[arg], self.test_case_format[arg])
        stream = open(kwargs.get('stream'))
        inst = self.cls()
        inst.read_input(stream)
        assert isinstance(inst.data, list)