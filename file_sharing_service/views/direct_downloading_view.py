from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service.configs.flask_configuration import api
from flask_restful import Resource
from flask import request, send_file


class DownloadingLinkView(Resource):
    def get(self):
        file_data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }
        print('qweqw')
        emit_sending(
            file_data,
            queue_name=rabbit_configuration.file_queue_name,
            routing_key=rabbit_configuration.file_routing_key
        )

        return 200


class DirectDownloadingView(Resource):
    def get(self):
        filepath = request.args.get('filepath', type=str)
        return send_file(filepath, as_attachment=True)


api.add_resource(DirectDownloadingView, '/download')
api.add_resource(DownloadingLinkView, '/download-link')
