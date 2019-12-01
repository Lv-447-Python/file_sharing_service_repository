"""Flask configs"""
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


APP = Flask(__name__)
API = Api(APP)

POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_USER = 'postgres'
POSTGRES_PW = 'Not4U^3l'
POSTGRES_DB = 'Sharing_DB'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PW,
    url=POSTGRES_URL,
    db=POSTGRES_DB
)

# APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(APP)
ma = Marshmallow(APP)
