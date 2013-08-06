"""
Preprocess data before sending to algorithms
"""

from __future__ import division
from base import Task
from percept.fields.base import List, Complex
import numpy as np
from percept.conf.base import settings
from percept.utils.models import RegistryCategories
from percept.tests.framework import NormalizationTester
import os
from percept.utils.input import DataFormats
import logging
from pandas import read_csv

log = logging.getLogger(__name__)

def is_number(n):
    try:
        n.astype(float)
        return True
    except ValueError:
        return False

class ReadCSV(Task):
    data = Complex()
    target = Complex()
    help_text = "Example class to read in CSV files."
    category = RegistryCategories.preprocessors

    def read_data(self, data):
        for d in data.keys():
            if "file" in d:
                name = d.replace("file","")
                data[name] = self.read_frame(data[d])
        return data

    def read_frame(self, ifile):
        df = read_csv(ifile)
        for i in xrange(0,df.shape[1]):
            if is_number(df.iloc[:,i]):
                df.iloc[:,i] = df.iloc[:,i].astype(float)
        return df

    def train(self,datafile,targetfile,**kwargs):
        self.data = self.read_frame(datafile)
        self.target = self.read_frame(targetfile)

    def predict(self, test_data,**kwargs):
        return self.read_data(test_data)

class Normalize(Task):
    """
    Normalize values by reducing standard deviation to 1 and mean to 0
    """
    column_means = List()
    column_stdevs = List()
    category = RegistryCategories.preprocessors
    tester = NormalizationTester
    test_cases = [{'stream' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/data/csv/1/data.csv'))}]
    data = Complex()

    help_text = "Example class to normalize input values."

    def train(self, data, **kwargs):
        """
        Calculate the standard deviations and means in the training data
        """
        self.data = data
        for i in xrange(0,data.shape[1]):
            column_mean = np.mean(data.icol(i))
            column_stdev = np.std(data.icol(i))

            #Have to do += or "list" type will fail (ie with append)
            self.column_means += [column_mean]
            self.column_stdevs += [column_stdev]

        self.data = self.predict(data)

    def predict(self, test_data, **kwargs):
        """
        Adjust new input by the values in the training data
        """
        if test_data.shape[1]!=self.data.shape[1]:
            raise Exception("Test data has different number of columns than training data.")
        for i in xrange(0,test_data.shape[1]):
            test_data.loc[:,i] = test_data.icol(i) - self.column_means[i]
            if int(self.column_stdevs[i])!=0:
                test_data.loc[:,i] = test_data.icol(i) / self.column_stdevs[i]
        return test_data