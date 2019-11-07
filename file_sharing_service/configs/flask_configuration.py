from flask import Flask
from flask_restful import Api
from flask_mail import Mail

app = Flask(__name__)
api = Api(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'testingforserve@gmail.com'
app.config['MAIL_PASSWORD'] = 'StrongPassword98'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
