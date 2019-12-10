"""View for sending email with file"""
from flask import request, make_response, jsonify
from flask_api import status
from flask_restful import Resource
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service import API
from file_sharing_service.configs import rabbit_configuration


class EmailSendingView(Resource):
    def get(self):
        if 'filename' not in request.args:
            return make_response(jsonify({
                'message': 'There is no filename in your request'
            }),
                status.HTTP_400_BAD_REQUEST)

        if 'email' not in request.args:
            return make_response(jsonify({
                'message': 'There is no email in your request'
            }),
                status.HTTP_400_BAD_REQUEST)

        file_data = {
            'filename': request.args.get('filename'),
            'email': request.args.get('email')
        }

        emit_sending(
            file_data,
            queue_name=rabbit_configuration.EMAIL_QUEUE_NAME,
            routing_key=rabbit_configuration.EMAIL_ROUTING_KEY
        )

        return make_response(jsonify({
            'message': 'Message was sent to the queue ' + rabbit_configuration.EMAIL_QUEUE_NAME
        }),
            status.HTTP_200_OK)


API.add_resource(EmailSendingView, '/email')
