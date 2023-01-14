import os, sys
import json
from flask import Flask, request, abort,  render_template

from premium.logger import logging
from premium.exception import PremiumException
from premium.predictor import Predictor, PremiumData

from premium.entity import config_entity, artifact_entity
from premium.pipeline.training_pipeline import start_training_pipeline


INSURANCE_DATA_KEY = "premium_data"
EXPENSES_KEY = "expenses"


app = Flask(__name__)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        INSURANCE_DATA_KEY: None,
        EXPENSES_KEY: None
    }

    if request.method == 'POST':
        age = float(request.form['age'])
        sex = str(request.form['sex'])
        bmi = float(request.form['bmi'])
        children = float(request.form['children'])
        smoker = str(request.form['smoker'])
        region = str(request.form['region'])
        
        premium_data = PremiumData(age=age,
                                   sex=sex,
                                   bmi=bmi,
                                   children=children,
                                   smoker=smoker,
                                   region=region,
                                   )

        premium_df = premium_data.get_input_data_frame()
        premium_predictor = Predictor()
        expenses = premium_predictor.predict(X=premium_df)
        context = {
            INSURANCE_DATA_KEY: premium_data.get_input_data_dict(),
            EXPENSES_KEY: expenses,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route("/", methods = ['GET', 'POST'])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        PremiumException(e, sys)

if __name__=="__main__":
    app.run(host="0.0.0.0", debug = True)