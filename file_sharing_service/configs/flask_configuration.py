from flask import Flask
from flask_restful import Api
from flask_mail import Mail

app = Flask(__name__)
api = Api(app)
mail = Mail(app)
