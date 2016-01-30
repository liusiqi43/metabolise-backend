#!/usr/local/bin/python
# coding: utf-8

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import median_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import classification_report

import time
import logging
import sys
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOG = logging.getLogger('training')

def _descritize(y, scale, lower = 5, upper = 3000):
    y = np.asarray(y)
    y = np.clip(scale * np.round(y/scale, 1), lower, upper).astype(int)
    y = ["%d" % cls for cls in y]
    return y

class Trainer(object):
    def __init__(self, x, y, train_ratio):
        sample_train = int(train_ratio * len(x))
        self._x_train = x[:sample_train]
        self._y_train = y[:sample_train]

        self._x_test = x[len(x) - sample_train:]
        self._y_test = y[len(y) - sample_train:]

        self._trained = False
        self._model = None

    def Train(self):
        self.Fit()
        x_train = self.Preprocess(self._x_train)
        self._model = self.Learn(x_train, self._y_train)
        self._trained = True

    def Predict(self, x):
        if not self._trained:
            raise RuntimeError(
                'Prediction requested but model is not trained yet.')
        x_test = self.Preprocess(x)
        return self._model.predict(x_test)

    def PredictProba(self, x):
        if not self._trained:
            raise RuntimeError(
                'Prediction requested but model is not trained yet.')
        x_test = self.Preprocess(x)
        return self._model.predict_proba(x_test)


    def Report(self):
        if not self._trained:
            raise RuntimeError(
                'Report requested but model is not trained yet.')
        report = self.Eval()
        for k, v in report.iteritems():
            LOG.info('metric [%s] = %s', k, str(v))

    def Preprocess(self, x):
        return x

    def Fit(self):
        pass

    def Learn(self, x_train, y_train):
        raise NotImplementedError(
            'Learn() is not implemented by Trainer subclass.')

    def Eval(self):
        raise NotImplementedError(
            'Eval() is not implemented by Trainer subclass.')


class CaloriesRegressor(Trainer):
    def __init__(self, x, y, train_ratio):
        super(CaloriesRegressor, self).__init__(x, y, train_ratio)
        self._count_vec = CountVectorizer()
        self._tfidf_transformer = TfidfTransformer()

    def Fit(self):
        x_count = self._count_vec.fit_transform(self._x_train)
        self._tfidf_transformer.fit(x_count)

    def Preprocess(self, x):
        return self._tfidf_transformer.transform(self._count_vec.transform(x))

    def Learn(self, x_train, y_train):
        LOG.info('x_train.shape = %s', str(x_train.shape))
        LOG.info('len(y_train) = %d', len(y_train))

        clf = RandomForestRegressor(verbose=0, n_jobs=-1, n_estimators=10)
        LOG.info('Training...')
        clf.fit(x_train, y_train)
        LOG.info('Done...')
        return clf

    def Eval(self):
        LOG.info('Eval ...')
        y_pred = self.Predict(self._x_test)
        return {
            'median_absolute_error':
            median_absolute_error(self._y_test, y_pred),
            'mean_squared_error': mean_squared_error(self._y_test, y_pred),
            'explained_variance_score':
            explained_variance_score(self._y_test, y_pred),
        }


class CaloriesClassifier(Trainer):
    def __init__(self, x, y, train_ratio):
        super(CaloriesClassifier, self).__init__(x, y, train_ratio)
        self._count_vec = CountVectorizer()
        self._tfidf_transformer = TfidfTransformer()
        self._y_train = _descritize(self._y_train, 100)
        self._y_test = _descritize(self._y_test, 100)

    def Fit(self):
        x_count = self._count_vec.fit_transform(self._x_train)
        self._tfidf_transformer.fit(x_count)

    def Preprocess(self, x):
        print x[0]
        return self._tfidf_transformer.transform(self._count_vec.transform(x))

    def Learn(self, x_train, y_train):
        LOG.info('x_train.shape = %s', str(x_train.shape))
        LOG.info('len(y_train) = %d', len(y_train))

        clf = RandomForestClassifier(verbose=0, n_jobs=-1, n_estimators=10)
        LOG.info('Training...')
        clf.fit(x_train, y_train)
        LOG.info('Done...')
        return clf

    def Eval(self):
        LOG.info('Eval ...')
        y_pred = self.Predict(self._x_test)
        return {
            'misclass': np.mean(y_pred != self._y_test),
            'report': classification_report(self._y_test, y_pred,
                                            target_names=self._model.classes_)
        }

class UnitClassifier(Trainer):
    def __init__(self, x, y, train_ratio):
        super(UnitClassifier, self).__init__(x, y, train_ratio)
        self._count_vec = CountVectorizer()
        self._tfidf_transformer = TfidfTransformer()

    def Fit(self):
        x_count = self._count_vec.fit_transform(self._x_train)
        self._tfidf_transformer.fit(x_count)

    def Preprocess(self, x):
        return self._tfidf_transformer.transform(self._count_vec.transform(x))

    def Learn(self, x_train, y_train):
        LOG.info('x_train.shape = %s', str(x_train.shape))
        LOG.info('len(y_train) = %d', len(y_train))

        clf = RandomForestClassifier(verbose=0, n_jobs=-1, n_estimators=10)
        LOG.info('Training...')
        clf.fit(x_train, y_train)
        LOG.info('Done...')
        return clf

    def Eval(self):
        LOG.info('Eval ...')
        y_pred = self.Predict(self._x_test)
        return {
            'misclass': np.mean(y_pred != self._y_test),
            'report': classification_report(self._y_test, y_pred,
                                            target_names=self._model.classes_)
        }
