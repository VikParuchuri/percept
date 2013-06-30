from base import Task
from fields.base import Complex, List
import numpy as np
from sklearn import svm
from conf.base import settings
from utils.models import RegistryCategories
from tests.framework import SVMTester
import os
from utils.input import DataFormats

import logging

log = logging.getLogger(__name__)

class SVMTrain(Task):
    colnames = List()
    clf = Complex()
    category = RegistryCategories.preprocessors
    algorithm = svm.SVC
    args = {'C' : 1.0}
    tester = SVMTester
    test_cases = [
        {
            'data' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1/data.csv')),
            'target' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1/target.csv')),
            'dataformat' : DataFormats.csv
        }
    ]

    def train(self, data, target, **kwargs):
        self.colnames = [t for t in data.columns]

        C = kwargs.get('C',1)
        self.clf = self.algorithm(C=C)
        log.info(data)
        log.info(target)
        self.clf.fit(data, target)

    def predict(self, test_data, **kwargs):
        test_data = test_data
        log.info(test_data)
        return self.clf.predict(test_data)