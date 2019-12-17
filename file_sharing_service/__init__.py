"""Flask configs"""
import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


APP = Flask(__name__)
API = Api(APP)

HOST = '0.0.0.0'
PORT = 5000

POSTGRES_URL = '127.0.0.1'
POSTGRES_PORT = 5432

POSTGRES_USER = 'postgres'
POSTGRES_PW = 'Not4U^3l'
POSTGRES_DB = 'Sharing_DB'

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PW,
    url=POSTGRES_URL,
    port=POSTGRES_PORT,
    db=POSTGRES_DB
)

APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['UPLOAD_FOLDER'] = 'generated_files/'

UPLOADS_DIR = os.path.join(os.path.dirname(APP.root_path), APP.config['UPLOAD_FOLDER'])

DATABASE = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)
MIGRATE = Migrate(APP, DATABASE)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
