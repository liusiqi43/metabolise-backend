from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug import secure_filename
from sklearn.externals import joblib

from train import Trainer, UnitClassifier, CaloriesRegressor
from predict import predict_cal, predict_units
from speech import get_text
from hodclient import *

import time

app = Flask(__name__)
api = Api(app)

calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                 % time.strftime('%Y%m%d'))
unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                              % time.strftime('%Y%m%d'))

def speech_to_text(filename):
  with open(filename, 'rb') as audio:
    response = request.post(url, files={'file': audio}, data={'apikey': api_key})
  print response

class Calorie(Resource):
  def get(self):
    dish = request.args.get('dish')
    predicted_cals = predict_cal(calories_regressor, dish)
    predicted_units = predict_units(unit_classifier, dish, 1)
    print predicted_cals, predicted_units
    result = {'calories': int(predicted_cals[0]), 
              'units': predicted_units[0][1]}
    return result

class Speech(Resource):
  def post(self):
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save('./' + filename)
    result = {'text': get_text(filename)}
    return result

api.add_resource(Calorie, '/')

if __name__ == '__main__':
  app.run(debug=True)
