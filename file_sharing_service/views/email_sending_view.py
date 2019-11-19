from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs.flask_configuration import api
from file_sharing_service.configs import rabbit_configuration
from flask_restful import Resource
from flask_restful import http_status_message
from flask import request


class EmailSendingView(Resource):
    def get(self):
        file_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }

        emit_sending(
            file_data,
            queue_name=rabbit_configuration.email_queue_name,
            routing_key=rabbit_configuration.email_routing_key
        )

        return http_status_message(200)


api.add_resource(EmailSendingView, '/email')
