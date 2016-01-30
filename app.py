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

class Metaboliser(Resource):
  def get(self):
      return {todo_id: todos[todo_id]}

  def put(self):
    predicted_cals = predict_cal(calories_regressor, request.form['dish'])
    print predicted_cals
    return {'calories': predicted_cals[0]}

api.add_resource(Metaboliser, '/')

if __name__ == '__main__':
  app.run(debug=True)
