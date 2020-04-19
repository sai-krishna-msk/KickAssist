from ml_model.model import KickModel
import numpy as np
import pandas as pd
import eli5
import joblib
import flask 
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

model_oh = joblib.load('ml_model/estimators/model_oh.sav')
model_hel = joblib.load('ml_model/estimators/model_hel.sav')
encoder_oh = joblib.load('ml_model/estimators/encoder_oh.sav')
encoder_hel = joblib.load('ml_model/estimators/encoder_hel.sav')
encoder_label = joblib.load('ml_model/estimators/encoder_label.sav')


def get_predict(launch_date , deadline_date , goal , subcategory , category , currency , country , description, rewards):
    pred_dict={
    "launched_at":launch_date,
    "deadline":deadline_date, 
    "goal":int(goal),
    "sub_category":subcategory,
    "category":category,
    "currency":currency,
    "location_country":country,
    "blurb":description, 
    "rewards":[] 
    }
    try:
        for reward in rewards.split(","):
            pred_dict["rewards"].append(int(reward))
    except Exception as e:
        raise Exception(f"Error sanatizing rewards with {e} error")

    return pred_dict

@app.route('/predict/<launch_date>/<deadline_date>/<goal>/<subcategory>/<category>/<currency>/<country>/<description>/<rewards>')
def GetURL(launch_date , deadline_date , goal , subcategory , category , currency , country , description, rewards):
    pred_dict = get_predict(launch_date , deadline_date , goal , subcategory , category , currency , country , description, rewards)

    obj = KickModel(model_oh , model_hel , encoder_oh , encoder_hel , encoder_label)
    obj.load_data(pred_dict)
    obj.pred()
    oh_pred = float(obj.pred_oh[0][1])
    hel_pred = float(obj.pred_hel[0][1])

    response = {
    "prediction_oh":oh_pred,
    "prediction_hel":hel_pred,
    "prediction_oh_df":obj.pred_oh_intr.to_dict(), 
    "prediction_hel_intr":obj.pred_hel_intr.to_dict()
    }
    return response



if __name__=="__main__":
	app.run(debug =True)