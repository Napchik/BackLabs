from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from config import JWT_SECRET_KEY

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

import src.views
import src.models

