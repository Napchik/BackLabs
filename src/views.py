from flask import Flask, jsonify, request
from src.data import User, users
from src.data import Category, categories
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


@app.post("/category")
def create_category():
    category_data = request.get_json()
    category = Category(**category_data)
    categories[category.id] = category
    return dataclasses.asdict(category)


@app.get("/user/<id>")
def get_user(id):
    return dataclasses.asdict(users[id])


@app.get("/category/<id>")
def get_category(id):
    return dataclasses.asdict(categories[id])


@app.get("/users")
def get_users():
    return list(users.values())


@app.get("/categories")
def get_categories():
    return list(categories.values())


@app.delete("/user/<id>")
def delete_user(id):
    return dataclasses.asdict(users.pop(id))


@app.delete("/category/<id>")
def delete_category(id):
    return dataclasses.asdict(categories.pop(id))
