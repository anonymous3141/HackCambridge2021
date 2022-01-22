from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('generic.html')

@app.route("/dank")
def dank_memes():
    return "<p>Dank Memes!</p>"
