from flask import Flask
from flask import render_template, make_response
import json

app = Flask(__name__)
Global = None


def import_global(_global):
    global Global
    Global = _global


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/ready')
def check_ready():
    response = make_response(json.dumps(Global.finished))
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response
