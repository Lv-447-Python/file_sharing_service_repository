"""View for sending email with file"""
from flask import request
from flask_restful import Resource
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service import API
from file_sharing_service.configs import rabbit_configuration


class EmailSendingView(Resource):
    def get(self):
        file_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int),
            'email': request.args.get('email', type=str)
        }

        emit_sending(
            file_data,
            queue_name=rabbit_configuration.EMAIL_QUEUE_NAME,
            routing_key=rabbit_configuration.EMAIL_ROUTING_KEY
        )

        return {
            'status': 200,
            'msg': 'Message was sent to the queue ' + rabbit_configuration.EMAIL_QUEUE_NAME
        }


API.add_resource(EmailSendingView, '/email')
