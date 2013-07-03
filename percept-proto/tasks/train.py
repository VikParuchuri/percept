"""
Machine learning algorithms to train and predict
"""

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
    """
    A class to train a support vector machine algorithm
    """
    colnames = List()
    clf = Complex()
    category = RegistryCategories.algorithms
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
    help_text = "Example class to train and predict with SVM."

    def train(self, data, target, **kwargs):
        self.colnames = [t for t in data.columns]

        C = kwargs.get('C',1)

        #When doing self.clf =clf , __set__ is called on the field.
        # But, when doing self.clf = self.algorithm() and self.clf.fit(), __set__ is not called.
        # Work around this by doing the fit logic on a local variable, and then assigning to self.clf,
        clf = self.algorithm(C=C)
        clf.fit(data, target)
        self.clf = clf

    def predict(self, test_data, **kwargs):
        test_data = test_data
        return self.clf.predict(test_data)