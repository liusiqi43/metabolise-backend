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
import pickle
import logging
import sys
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOG = logging.getLogger('training')


class Trainer(object):
    def __init__(self, x, y, train_ratio):
        sample_train = int(train_ratio * len(x))
        print 'x[0]', x[0], 'y[0]', y[0]
        self._x_train = x[:sample_train]
        self._y_train = y[:sample_train]

        self._x_test = x[:len(x) - sample_train]
        self._y_test = y[:len(y) - sample_train]

        self._trained = False
        self._model = None

    def Train(self):
        self.Fit()
        x_train = self.Preprocess(self._x_train)
        print 'preprocessed x_train[0]: ', x_train[0]
        self._model = self.Learn(x_train, self._y_train)
        self._trained = True

    def Predict(self, x):
        if not self._trained:
            raise RuntimeError(
                'Prediction requested but model is not trained yet.')
        x_test = self.Preprocess(x)
        return self._model.predict(x_test)

    def Report(self):
        if not self._trained:
            raise RuntimeError(
                'Report requested but model is not trained yet.')
        report = self.Eval()
        for k, v in report.iteritems():
            LOG.info('metric [%s] = %s', k, repr(v))

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


class CaloriesTrainer(Trainer):
    def __init__(self, x, y, train_ratio):
        super(CaloriesTrainer, self).__init__(x, y, train_ratio)
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


class UnitTrainer(Trainer):
    def __init__(self, x, y, train_ratio):
        super(UnitTrainer, self).__init__(x, y, train_ratio)
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


if __name__ == '__main__':
    from training_set import get_cal_data, get_unit_data
    from pymongo import MongoClient

    x_cal, y_cal = get_cal_data(MongoClient())
    calories_trainer = CaloriesTrainer(x_cal, y_cal, 0.8)
    calories_trainer.Train()
    calories_trainer.Report()
    pickle.dump(calories_trainer, open('models/calories_trainer_%s_1.pkl' %
                                       time.strftime('%Y%m%d'), 'wb'))

    x_unit, y_unit = get_unit_data(MongoClient())
    unit_trainer = UnitTrainer(x_unit, y_unit, 0.8)
    unit_trainer.Train()
    unit_trainer.Report()
    pickle.dump(unit_trainer,
                open('models/unit_trainer_%s.pkl' % time.strftime('%Y%m%d'),
                     'wb'))
