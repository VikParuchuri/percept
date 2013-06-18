from base import Task
from fields.base import Complex, List
import numpy as np
from sklearn import svm
from conf.base import settings
from utils.models import RegistryCategories

class SVMTrain(Task):
    colnames = List()
    clf = Complex()
    category = RegistryCategories.preprocessors
    algorithm = svm.SVC()
    args = {'C' : 1.0, 'target_name' : 'target'}

    def train(self, data, **kwargs):
        self.colnames = [t for t in data.columns if t!=kwargs['target_name']]

        C = kwargs['C']
        self.clf = self.algorithm(C=C)
        self.clf.fit(data[self.colnames],data[kwargs['target_name']])

    def predict(self, test_data, **kwargs):
        test_data = test_data[self.colnames]
        return self.clf.predict(test_data)