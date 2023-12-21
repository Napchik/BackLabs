from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from datetime import datetime
from src.schemas import UserSchema, CategorySchema, RecordSchema, CurrencySchema
from src.models import User, Category, Record, Currency
from src import db, app

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route("/healthcheck")
def healthcheck():
    resp = jsonify(date=datetime.now(), status="OK")
    resp.status_code = 200
    return resp


# =======================USERS===========================
@app.post("/user")
def create_user():
    data = request.get_json()

    user_schema = UserSchema()
    try:
        user_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    default_currency_id = data.get("default_currency_id")
    default_currency = Currency.query.filter_by(id=default_currency_id).first()

    if default_currency_id is None:
        default_currency = Currency.query.filter_by(name="Default Currency").first()
        if not default_currency:
            # Валюта за замовчуванням не існує, тому створіть її
            default_currency = Currency(name="Default Currency", symbol="UAH")
            db.session.add(default_currency)
            db.session.commit()
            default_currency = Currency.query.filter_by(name="Default Currency").first()

    new_user = User(
        username=user_data["username"],
        default_currency_id=default_currency.id
    )
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

        user_response = {
            'id': new_user.id,
            'username': new_user.username,
            'currency': new_user.default_currency.symbol if new_user.default_currency else None
        }
        return jsonify(user_response), 200


@app.get("/user/<id>")
def get_user(id):
    with app.app_context():
        user = User.query.get(id)

        if not user:
            return jsonify({'error': f'User with that {id} dosnt exist'}), 404

        user_data = {
            'id': user.id,
            'username': user.username,
            'currency': user.default_currency_id}

        return jsonify(user_data), 200


@app.get("/users")
def get_users():
    with app.app_context():
        users_data = {
            user.id: {"userid": user.id, "username": user.username, "currency": user.default_currency_id} for user in
            User.query.all()
        }
        return jsonify(users_data)


@app.delete("/user/<id>")
def delete_user(id):
    with app.app_context():
        user = User.query.get(id)

        if not user:
            return jsonify({'error': f'User with that {id} dosnt exist'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {id} deleted'}), 200


# =======================RECORDS===========================
@app.post("/record")
def create_record():
    data = request.get_json()
    record_schema = RecordSchema()
    try:
        record_data = record_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    user_id = record_data['user_id']
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Retrieve the currency_id from the associated user
    currency_id = user.default_currency_id

    new_record = Record(
        user_id=user_id,
        category_id=record_data['category_id'],
        sum=record_data['sum'],
        currency_id=currency_id
    )
    with app.app_context():
        db.session.add(new_record)
        db.session.commit()

        record_response = {
            "id": new_record.id,
            "user_id": new_record.user_id,
            "category_id": new_record.category_id,
            "sum": new_record.sum,
            "currency_id": new_record.currency_id
        }

        return jsonify(record_response), 200


@app.get("/recorduser")
def get_record_user():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({'error': 'Specify user_id or category_id'}), 400

    query = Record.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    need_records = query.all()
    print(need_records)
    records_data = {
        record.id: {
            "user_id": record.user_id,
            "category_id": record.category_id,
            "sum": record.sum,
            "currency_id": record.currency_id,
            "created_at": record.created_at
        } for record in need_records
    }
    return jsonify(records_data)


@app.get("/record/<id>")
def get_record(id):
    with app.app_context():
        record = Record.query.get(id)

        if not record:
            return jsonify({"error": f"Record {id} not found"}), 404

        record_data = {
            "id": record.id,
            "user_id": record.user_id,
            "category_id": record.category_id,
            "sum": record.sum,
            "currency_id": record.currency_id,
            "created_at": record.created_at
        }
        return jsonify(record_data), 200


@app.get("/records")
def get_records():
    with app.app_context():
        records_data = {
            "records": [
                {
                    "id": record.id,
                    "user_id": record.user_id,
                    "cat_id": record.category_id,
                    "sum": record.sum,
                    "currency_id": record.currency_id,
                    "created_at": record.created_at
                } for record in Record.query.all()
            ]
        }
        return jsonify(records_data)


@app.delete("/record/<id>")
def delete_record(id):
    with app.app_context():
        record = Record.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': f'Record {id} deleted'}), 200


# =======================CATEGORY===========================
@app.post("/category")
def create_category():
    data = request.get_json()
    cat_schema = CategorySchema()
    try:
        cat_data = cat_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    new_category = Category(name=cat_data["name"])
    with app.app_context():
        db.session.add(new_category)
        db.session.commit()

        category_response = {
            "id": new_category.id,
            "name": new_category.name
        }

        return jsonify(category_response), 200


@app.get("/categories")
def get_categories():
    with app.app_context():
        categories_data = {
            category.id: {"name": category.name} for category in Category.query.all()
        }
        return jsonify(categories_data)

@app.get("/category/<id>")
def get_category(id):
    with app.app_context():
        category = Category.query.get(id)

        if not category:
            return jsonify({"error": f"Category {id} not found"}), 404

        category_data = {
            "category_id": id,
            "category_name": category.name,
        }
        return jsonify(category_data), 200


@app.delete("/category/<id>")
def delete_category(id):
    with app.app_context():
        category = Category.query.get(id)

        if not category:
            return jsonify({'error': f'Category {id} not found'}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': f'Category {id} deleted'}), 200


# =======================CURRENCY===========================

@app.post("/currency")
def create_currency():
    data = request.get_json()
    currency_schema = CurrencySchema()
    try:
        currency_data = currency_schema.load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    new_currency = Currency(name=currency_data["name"], symbol=currency_data["symbol"])
    with app.app_context():
        db.session.add(new_currency)
        db.session.commit()

        currency_response = {
            "id": new_currency.id,
            "name": new_currency.name,
            "symbol": new_currency.symbol
        }
        return jsonify(currency_response), 200


@app.get("/currencies")
def get_currencies():
    with app.app_context():
        currencies_data = {
            currency.id: {"name": currency.name, "symbol": currency.symbol}
            for currency in Currency.query.all()
        }
        return jsonify(currencies_data)


@app.get("/currency/<id>")
def get_currency(id):
    with app.app_context():
        currency = Currency.query.filter_by(id=id).first()
    if currency:
        currency_data = {
            'id': currency.id,
            'name': currency.name,
            'symbol': currency.symbol
        }
        return jsonify(currency_data), 200
    else:
        return jsonify({'error': f'Currency {id} not found'}), 404


@app.delete("/currency/<id>")
def delete_currency(id):
    with app.app_context():
        currency = Currency.query.filter_by(id=id).first()
        if currency:
            db.session.delete(currency)
            db.session.commit()
            return jsonify({'message': f'Currency {id} deleted'}), 200
        else:
            return jsonify({'error': f'Currency {id} not found'}), 404
