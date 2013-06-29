from base import Task
from fields.base import List, Complex
import numpy as np
from conf.base import settings
from utils.models import RegistryCategories
from tests.framework import NormalizationTester
import os
from utils.input import DataFormats
import logging

log = logging.getLogger(__name__)

class Normalize(Task):
    column_means = List()
    column_stdevs = List()
    category = RegistryCategories.preprocessors
    tester = NormalizationTester
    test_cases = [{'stream' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1.csv')), 'dataformat' : DataFormats.csv}]
    data = Complex()

    def train(self, data, **kwargs):
        self.data = data
        for i in xrange(0,data.shape[1]):
            column_mean = np.mean(data.icol(i))
            column_stdev = np.std(data.icol(i))

            #Have to do += or "list" type will fail (ie with append)
            self.column_means += [column_mean]
            self.column_stdevs += [column_stdev]

        self.data = np.asarray(self.predict(data))

    def predict(self, test_data, **kwargs):
        if test_data.shape[1]!=self.data.shape[1]:
            raise Exception("Test data has different number of columns than training data.")
        for i in xrange(0,test_data.shape[1]):
            log.info(test_data.icol(i))
            test_data.loc[:,i] = test_data.icol(i).astype(float) - self.column_means[i]
            if int(self.column_stdevs[i])!=0:
                test_data.loc[:,i] = test_data.icol(i).astype(float) / self.column_stdevs[i]
        return test_data