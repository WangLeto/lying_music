from flask import Flask

app = Flask(__name__)
Global = None


def import_global(_global):
    global Global
    Global = _global


@app.route('/')
def hello_world():
    return 'Hello World! ' + str(Global.finished)
