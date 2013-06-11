from base import Task
from fields.base import List
import numpy as np
from conf.base import settings
from utils.models import RegistryCategories

class Normalize(Task):
    column_means = List()
    column_stdevs = List()
    category = RegistryCategories.preprocessors

    def train(self, **kwargs):
        self.column_means = []
        self.column_stdevs = []
        for i in xrange(0,self.data.shape[1]):
            column_mean = np.mean(self.data[i])
            column_stdev = np.std(self.data[i])
            self.column_means.append(column_mean)
            self.column_stdevs.append(column_stdev)

        self.data = self.predict(self.data)

    def predict(self, test_data, **kwargs):
        if test_data.shape[1]!=self.data.shape[1]:
            raise Exception("Test data has different number of columns than training data.")
        for i in xrange(0,test_data.shape[1]):
            test_data[i] = test_data[i] - self.column_means[i]
            if int(self.column_stdevs[i])!=0:
                test_data[i] = test_data[i] / self.column_stdevs[i]
        return test_data