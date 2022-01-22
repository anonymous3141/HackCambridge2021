from flask import Flask
from flask import render_template
from sentiment_score import get_sentiment_score
from allowance_predictor import predict
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

@app.route("/api/get_sentiment")
def get_sentiment():
    # e.g /api/get_sentiment
    return str(get_sentiment_score())
