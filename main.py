from flask import Flask
from flask import render_template
from sentiment_score import get_sentiment_score
from allowance_predictor import predict
from electricity_predictor import elec_predict
import pandas as pd
import numpy as np
import datetime
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('generic.html')

@app.route("/dank")
def dank_memes():
    return "<p>Dank Memes!</p>"

@app.route("/api/allowance_predict/<history>")
def predict_allowance(history):
    # e.g /api/allowance_predict/1,2,3,4,5,6,7
    # 7 comma seperated values from old to new
    cleaned = [float(c) for c in history.split(',')]
    return str(predict(cleaned))

@app.route("/api/electricity_predict/<data>")
def predict_electricity(data):
    # input: average temp, min temp, max temp, humidity, forecasted rain
    # (cont) forecasted snow, day,month (int),year
    # i.e 9 comma seperated values
    # temp temp_min temp_max humidity rain_1h snow_3h month weekday (2015/1/1 = 0)
    cleaned = [float(c) for c in data.split(',')]
    
    # convert to data format fed into xgboost
    cleaned[4]/=24
    cleaned[5]/=8
    day_week = datetime.datetime(int(cleaned[-1]), int(cleaned[-2]), int(cleaned[-3])).weekday()
    day_week = (day_week + 4) % 7 # thursday is 0 in XGboost
    dat = cleaned[:-3]
    dat.append(cleaned[-2])
    dat.append(day_week)
    plug = pd.DataFrame({"temp": [dat[0]],
                     "temp_min": [dat[1]],
                     "temp_max": [dat[2]],
                     "humidity": [dat[3]],
                     "rain_1h": [dat[4]],
                     "snow_3h": [dat[5]],
                     "month": [dat[6]],
                     "weekday": [dat[7]]})
                     
    return str(elec_predict(plug))

@app.route("/api/get_sentiment")
def get_sentiment():
    # e.g /api/get_sentiment
    return str(get_sentiment_score())

@app.route("/api/get_data")
def get_data(as_string=True):
    # temporary stopgap
    if as_string:
        return str(pd.read_csv("static/EMBER_Coal2Clean_EUETSPrices.csv")['Price'].to_numpy())
    else:
        return pd.read_csv("static/EMBER_Coal2Clean_EUETSPrices.csv")['Price'].to_numpy()

