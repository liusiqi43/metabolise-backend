from train import Trainer, UnitClassifier, CaloriesRegressor
from sklearn.externals import joblib

import time

def predict_cal(predictor, dish_with_unit):
    predicted_cal = predictor.Predict([dish_with_unit])
    return predicted_cal

def predict_units(predictor, dish_without_unit, topn):
    blacklist = set(['g', 'oz', 'fl oz'])
    predicted_units = predictor.PredictProba([dish_without_unit])
    units = predicted_units[0]
    predicted_units = []
    for i, u in enumerate(units):
        if u <= 0 or predictor._model.classes_[i] in blacklist:
            continue
        predicted_units.append((u, predictor._model.classes_[i]))
    predicted_units = sorted(predicted_units, reverse = True)
    return ['serving'] if len(predicted_units) == 0 else predicted_units[:topn]

def main():
    calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                  % time.strftime('%Y%m%d'))
    unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                                  % time.strftime('%Y%m%d'))

    while True:
        name = raw_input('Name of the dish? ')
        print 'calories: ', predict_cal(calories_regressor, name)
        print 'units: ', predict_units(unit_classifier, name, 5)


if __name__ == '__main__':
    main()

