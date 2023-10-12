from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

health_status = True

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/healthcheck")
def healthcheck():
    if health_status:
        resp = jsonify(date=datetime.now(), status="OK")
        resp.status_code = 200
    else:
        resp = jsonify(date=datetime.now(), status="FAIL")
        resp.status_code = 500
    return resp
