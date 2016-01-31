#!/usr/local/bin/python
# coding: utf-8

import time

from training_set import get_cal_data, get_unit_data
from pymongo import MongoClient

from train import Trainer, UnitClassifier, CaloriesRegressor
from sklearn.externals import joblib


if __name__ == '__main__':
    blacklist = set(['g', 'oz', 'fl oz', 'gram', 'tbsp'])
    # x_cal, y_cal = get_cal_data(MongoClient(), blacklist)
    # calories_classifier = CaloriesClassifier(x_cal, y_cal, 0.8)
    # calories_classifier.Train()
    # calories_classifier.Report()
    # joblib.dump(calories_classifier,
    #             'models/calories_classifier_%s.pkl' % time.strftime('%Y%m%d'))

    x_cal, y_cal = get_cal_data(MongoClient(), blacklist)
    calories_trainer = CaloriesRegressor(x_cal, y_cal, 0.9)
    calories_trainer.Train()
    calories_trainer.Report()
    joblib.dump(calories_trainer, 'models/calories_regressor_%s.pkl'
                % time.strftime('%Y%m%d'))

    x_unit, y_unit = get_unit_data(MongoClient(), blacklist)
    unit_trainer = UnitClassifier(x_unit, y_unit, 0.9)
    unit_trainer.Train()
    unit_trainer.Report()
    joblib.dump(unit_trainer,
                'models/unit_classifier_%s.pkl' % time.strftime('%Y%m%d'))
