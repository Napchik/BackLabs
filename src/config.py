import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = ['HS256']
SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

SQLALCHEMY_TRACK_MODIFICATIONS = False
