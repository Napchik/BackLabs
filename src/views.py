from flask import Flask, jsonify, request
from src.data import User, users
import dataclasses
from datetime import datetime

app = Flask(__name__)


@app.route("/healthcheck")
def healthcheck():
    resp = jsonify(date=datetime.now(), status="OK")
    resp.status_code = 200
    return resp


@app.post("/user")
def create_user():
    user_data = request.get_json()
    user = User(**user_data)
    users[user.id] = user
    return dataclasses.asdict(user)


@app.get("/user/<id>")
def get_user(id):
    return dataclasses.asdict(users[id])


@app.get("/users")
def get_users():
    return list(users.values())


@app.delete("/user/<id>")
def delete_user(id):
    return dataclasses.asdict(users.pop(id))
