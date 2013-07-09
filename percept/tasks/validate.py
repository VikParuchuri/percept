"""
Structures to validate and estimate error
"""

from base import Task
from percept.fields.base import Complex, List, Float
import numpy as np
from percept.conf.base import settings
from percept.utils.models import RegistryCategories, get_namespace
import os
from percept.utils.input import DataFormats
from itertools import chain
import math
import random
import pandas as pd

def make_df(datalist, labels, name_prefix=""):
    df = pd.DataFrame(datalist).T
    if name_prefix!="":
        labels = [name_prefix + "_" + l for l in labels]
    labels = [l.replace(" ", "_").lower() for l in labels]
    df.columns = labels
    df.index = range(df.shape[0])
    return df

class Validate(Task):
    data = Complex()
    results = Complex()
    error = Float()
    importances = Complex()
    importance = Complex()
    column_names = List()

    data_format = DataFormats.dataframe

    category = RegistryCategories.preprocessors
    namespace = get_namespace(__module__)

    help_text = "Validate."

    def cross_validate(self, data, non_predictors, **kwargs):
        nfolds = kwargs.get('nfolds', 3)
        algo = kwargs.get('algo')
        seed = kwargs.get('seed', 1)
        data_len = data.shape[0]
        counter = 0
        fold_length = int(math.floor(data_len/nfolds))
        folds = []
        data_seq = list(xrange(0,data_len))
        random.seed(seed)
        random.shuffle(data_seq)

        for fold in xrange(0, nfolds):
            start = counter

            end = counter + fold_length
            if fold == (nfolds-1):
                end = data_len
            folds.append(data_seq[start:end])
            counter += fold_length

        results = []
        data.index = range(data.shape[0])
        self.importances = []
        for (i,fold) in enumerate(folds):
            predict_data = data.iloc[fold,:]
            out_indices = list(chain.from_iterable(folds[:i] + folds[(i + 1):]))
            train_data = data.iloc[out_indices,:]
            alg = algo()
            target = train_data['next_year_wins']
            train_data = train_data[[l for l in list(train_data.columns) if l not in non_predictors]]
            predict_data = predict_data[[l for l in list(predict_data.columns) if l not in non_predictors]]
            clf = alg.train(train_data,target,**algo.args)
            results.append(alg.predict(predict_data))
            self.importances.append(clf.feature_importances_)
        return results, folds

    def train(self, data, target, **kwargs):
        """
        Used in the training phase.  Override.
        """
        non_predictors = [i.replace(" ", "_").lower() for i in list(set(data['team']))] + ["team", "next_year_wins"]
        self.column_names = [l for l in list(data.columns) if l not in non_predictors]
        results, folds = self.cross_validate(data, non_predictors, **kwargs)
        self.gather_results(results, folds, data)

    def gather_results(self, results, folds, data):
        full_results = list(chain.from_iterable(results))
        full_indices = list(chain.from_iterable(folds))
        partial_result_df = make_df([full_results, full_indices], ["result", "index"])
        partial_result_df = partial_result_df.sort(["index"])
        partial_result_df.index = range(partial_result_df.shape[0])
        result_df = pd.concat([partial_result_df, data[['next_year_wins', 'team', 'year', 'total_wins']]], axis=1)
        result_df = result_df[(result_df['next_year_wins']>0) & result_df['total_wins']>0]
        self.results = result_df
        self.calc_error(result_df)
        self.calc_importance(self.importances, self.column_names)

    def calc_error(self, result_df):
        filtered_df = result_df[result_df['year']<np.max(result_df['year'])]
        self.error = np.mean(np.abs(filtered_df['result'] - filtered_df['next_year_wins']))

    def calc_importance(self, importances, col_names):
        importance_frame = pd.DataFrame(importances)
        importance_frame.columns = col_names
        self.importance = importance_frame.mean(axis=0)
        self.importance.sort(0)

    def predict(self, data, **kwargs):
        """
        Used in the predict phase, after training.  Override
        """

        pass