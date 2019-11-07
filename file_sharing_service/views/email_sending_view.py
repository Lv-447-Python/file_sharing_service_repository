from flask import send_file
from file_sharing_service.configs.flask_configuration import api, mail
from flask_restful import Resource
from flask_mail import Message


class EmailSendingView(Resource):
    def get(self):
        msg = Message("Hello",
                      sender="testingforserve@gmail.com",
                      recipients=["qwertttyew@dmailpro.net"])
        msg.body = 'asdasd'
        mail.send(msg)

        return 'message'


api.add_resource(EmailSendingView, '/email')
