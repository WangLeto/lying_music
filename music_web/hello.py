from flask import Flask
from flask import render_template

app = Flask(__name__)
Global = None


def import_global(_global):
    global Global
    Global = _global


@app.route('/')
def hello_world():
    return render_template('index.html')
