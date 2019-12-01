"""View for generation link and downloading file"""
from flask import request, send_file
from flask_restful import Resource, http_status_message
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service import API


class DownloadingLinkView(Resource):
    def get(self):
        file_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }
        emit_sending(
            file_data,
            queue_name=rabbit_configuration.FILE_QUEUE_NAME,
            routing_key=rabbit_configuration.FILE_ROUTING_KEY
        )

        return {
            'status': 200,
            'msg': 'Message was sent to the queue ' + rabbit_configuration.FILE_QUEUE_NAME
        }


class DirectDownloadingView(Resource):
    def get(self):
        try:
            filepath = request.args.get('filepath', type=str)
            return send_file(filepath, as_attachment=True)
        except FileNotFoundError:
            return http_status_message(404)


API.add_resource(DirectDownloadingView, '/download')
API.add_resource(DownloadingLinkView, '/download-link')
