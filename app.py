from flask import Flask, request
from flask_restful import Resource, Api
from sklearn.externals import joblib

from train import Trainer, UnitClassifier, CaloriesRegressor
from predict import predict_cal, predict_units

import time

app = Flask(__name__)
api = Api(app)

calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                 % time.strftime('%Y%m%d'))
unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                              % time.strftime('%Y%m%d'))

api_key = 'your api key'
hpe_url = 'https://api.havenondemand.com/1/api/async/recognizespeech/v1?file={0}&apikey={1}'

def speech_to_text(filename):
  response = request.post(hpe_url.format(filename, api_key))
  print response

class Calorie(Resource):
  def get(self):
    dish = request.args.get('dish')
    predicted_cals = predict_cal(calories_regressor, dish)
    print predicted_cals
    return predicted_cals[0]

api.add_resource(Calorie, '/')

if __name__ == '__main__':
  app.run(debug=True)
