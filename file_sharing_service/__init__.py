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

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'sharing_db',
    'host': 'db',
    'port': '5432',
}
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['UPLOAD_FOLDER'] = 'generated_files/'

UPLOADS_DIR = os.path.join(os.path.dirname(APP.root_path), APP.config['UPLOAD_FOLDER'])

DATABASE = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)

MIGRATE = Migrate(APP, DATABASE)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)

from file_sharing_service.models.generated_file import GeneratedFile
