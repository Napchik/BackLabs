from flask import Flask, jsonify, request
from src.data import User, users
from src.data import Category, categories
from src.data import Record, records
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


@app.post("/record")
def create_record():
    record_data = request.get_json()
    record = Record(**record_data, created=str(datetime.now()))
    records[record.id] = record
    return dataclasses.asdict(record)


@app.get("/user/<id>")
def get_user(id):
    return dataclasses.asdict(users[id])


@app.get("/category/<id>")
def get_category(id):
    return dataclasses.asdict(categories[id])


@app.get("/record/<id>")
def get_record(id):
    return dataclasses.asdict(records[id])


@app.get("/users")
def get_users():
    return list(users.values())


@app.get("/categories")
def get_categories():
    return list(categories.values())


@app.get("/records")
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    if not user_id and not category_id:
        return {
            "error": "At least one of the following query parameters should be present: [user_id, category_id]"}, 404
    return list(filter(lambda r: not category_id or r.category_id == category_id,
                       filter(lambda r: not user_id or r.user_id == user_id,
                              records.values())))


@app.delete("/user/<id>")
def delete_user(id):
    return dataclasses.asdict(users.pop(id))


@app.delete("/category/<id>")
def delete_category(id):
    return dataclasses.asdict(categories.pop(id))


@app.delete("/record/<id>")
def delete_record(id):
    return dataclasses.asdict(records.pop(id))
