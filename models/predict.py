from train import Trainer, CaloriesClassifier
from sklearn.externals import joblib

import time

def predict_cal(dish_with_unit):
    predicted_cals = calories_classifier.Predict([dish_with_unit])
    return predicted_cals

if __name__ == '__main__':
    calories_classifier = joblib.load('models/calories_classifier_%s_joblib.pkl' %
                                      time.strftime('%Y%m%d'))

    while True:
        name = raw_input('Name of the dish? ')
        print predict_cal(name)
