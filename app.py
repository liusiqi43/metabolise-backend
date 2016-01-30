from flask import Flask, request
from flask_restful import Resource, Api
from train import Trainer, UnitClassifier, CaloriesRegressor
from sklearn.externals import joblib
import time

app = Flask(__name__)
api = Api(app)


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

calories_regressor = joblib.load('models/calories_regressor_%s.pkl'
                                 % time.strftime('%Y%m%d'))
unit_classifier = joblib.load('models/unit_classifier_%s.pkl'
                              % time.strftime('%Y%m%d'))

class Metaboliser(Resource):
  def get(self):
      return {todo_id: todos[todo_id]}

  def put(self):
    predicted_cals = predict_cal(request.form['dish'])
    print predicted_cals
    return {'calories': predicted_cals[0]}

api.add_resource(Metaboliser, '/')

if __name__ == '__main__':
  app.run(debug=True)