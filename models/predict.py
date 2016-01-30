from train import Trainer, UnitClassifier, CaloriesRegressor
from sklearn.externals import joblib

import time

def predict_cal(dish_with_unit):
    predicted_cal = calories_regressor.Predict([dish_with_unit])
    return predicted_cal

def predict_units(dish_without_unit, topn):
    predicted_units = unit_classifier.PredictProba([dish_without_unit])
    units = predicted_units[0]
    predicted_units = []
    for i, u in enumerate(units):
        if u <= 0:
            continue
        predicted_units.append((u, unit_classifier._model.classes_[i]))
    predicted_units = sorted(predicted_units, reverse = True)
    return predicted_units[:topn]



if __name__ == '__main__':
    calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                     % time.strftime('%Y%m%d'))
    unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                                  % time.strftime('%Y%m%d'))

    while True:
        name = raw_input('Name of the dish? ')
        print 'calories: ', predict_cal(name)
        print 'units: ', predict_units(name, 5)
