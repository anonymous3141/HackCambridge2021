from refresh_allowance_data import ALLOWANCE_DATA_PATH, start_allowance_data_updater, download_file, update_allowance_data, HISTORY_LENGTH
import refresh_allowance_data
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from sentiment_score import get_sentiment_score
from allowance_predictor import predict, predict_n_days_forward
import pandas as pd

app = Flask(__name__)

start_allowance_data_updater()

def array_to_json(arr):
    return str(arr.tolist())

@app.route("/")
def hello_world():
    return render_template('generic.html')


@app.route("/dank")
def dank_memes():
    return "<p>Dank Memes!</p>"


@app.route("/api/get_data")
def get_data(as_string=True):
    # temporary stopgap
    if as_string:
        return str(refresh_allowance_data.allowance_data_past_week)
    return refresh_allowance_data.allowance_data_past_week

@app.route("/api/get_predicted_data")
def get_predicted_data():
    # temporary stopgap
    result = predict_n_days_forward(7)
    print(array_to_json(result))
    return array_to_json(result)

@app.route("/api/get_historical_data")
def get_historical_data():
    # temporary stopgap
    result = refresh_allowance_data.allowance_data_past_week[-HISTORY_LENGTH:]
    print(array_to_json(result))
    return array_to_json(result)

@app.route("/api/allowance_predict/<history>")
def predict_allowance(history):
    # e.g /api/allowance_predict/1,2,3,4,5,6,7
    # 7 comma seperated values from old to new
    cleaned = [float(c) for c in history.split(',')]
    return str(predict(cleaned))


@app.route("/api/get_sentiment")
def get_sentiment():
    # e.g /api/get_sentiment
    return 69
    # return get_sentiment_score()


@app.route('/test', methods=['GET', 'POST'])
def getresponse():
    # GET request
    if request.method == 'GET':
        message = {'response': get_sentiment()}  # get_sentiment()
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200


if __name__ == '__main__':
    app.run()

