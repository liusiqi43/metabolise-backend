from train import Trainer, CaloriesTrainer

import time
import pickle
import logging
import sys
import numpy as np

calories_trainer = pickle.load(open('models/calories_trainer_%s_1.pkl' %
                                    time.strftime('%Y%m%d'), 'rb'))

unit_trainer = pickle.load(open('models/unit_trainer_%s.pkl' % time.strftime('%Y%m%d'),
                                'rb'))

while True:
    name = raw_input('Name of the dish? ')
    print 'Estimating for: ' + name
    predicted_units = unit_trainer.Predict(name)
    print predicted_units
    units = sorted([(u, unit_clf.classes_[i])
                    for i, u in enumerate(predicted_units[0]) if u > 0],
                   reverse=True)
    print 'Unit: %s' % str(units)

    predicted_cal = calories_trainer.Predict(name)
    print predicted_cal

    #for unit in units:
    #    unit_name = name + ' ' + unit[1]

    #    predicted_cal = calories_trainer.Predict(unit_name)
    #    print 'proba %f: %s = %s calories.' % (unit[0], unit_name,
    #                                           str(predicted_cal))
