from flask import Flask, request
from flask_restful import Resource, Api
from sklearn.externals import joblib

from train import Trainer, UnitClassifier, CaloriesRegressor

import time

app = Flask(__name__)
api = Api(app)

calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                 % time.strftime('%Y%m%d'))
unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                              % time.strftime('%Y%m%d'))

def predict_cal(predictor, dish_with_unit):
    predicted_cal = predictor.Predict([dish_with_unit])
    return predicted_cal

def predict_units(predictor, dish_without_unit, topn):
    predicted_units = predictor.PredictProba([dish_without_unit])
    units = predicted_units[0]
    predicted_units = []
    for i, u in enumerate(units):
        if u <= 0:
            continue
        predicted_units.append((u, unit_classifier._model.classes_[i]))
    predicted_units = sorted(predicted_units, reverse = True)
    return predicted_units[:topn]

api_key = 'your api key'
hpe_url = 'https://api.havenondemand.com/1/api/async/recognizespeech/v1?file={0}&apikey={1}'

def speech_to_text(filename):
  response = request.post(hpe_url.format(filename, api_key))
  print response

class Calorie(Resource):
  def get(self):
      return {todo_id: todos[todo_id]}

  def put(self):
    predicted_cals = predict_cal(calories_regressor, request.form['dish'])
    print predicted_cals
    return {'calories': predicted_cals[0]}

api.add_resource(Calorie, '/calorie')

if __name__ == '__main__':
  app.run(debug=True)
