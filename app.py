from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug import secure_filename
from sklearn.externals import joblib

from train import Trainer, UnitClassifier, CaloriesRegressor
from predict import predict_cal, predict_units
from speech import get_text

import time

app = Flask(__name__)
api = Api(app)

calories_regressor = joblib.load('models/calories_regressor_20160130.pkl')
unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                              % time.strftime('%Y%m%d'))

def get_results(dish):
  """Return dict of estimated calories and serving size of dish."""
  predicted_cals = predict_cal(calories_regressor, dish)
  predicted_units = predict_units(unit_classifier, dish, 1)
  result = {'calories': int(predicted_cals[0]), 
            'units': predicted_units[0][1]}
  return result

class Calorie(Resource):
  def get(self):
    dish = request.args.get('dish')
    dish = ' '.join(dish.split()[:-1])
    return get_results(dish)

class Speech(Resource):
  def post(self):
    f = request.files['file']
    f.save('test.mp3')
    f.close()
    return {'text': get_text('test.mp3')}

api.add_resource(Calorie, '/')
api.add_resource(Speech, '/speech')

if __name__ == '__main__':
  app.run(debug=True)
