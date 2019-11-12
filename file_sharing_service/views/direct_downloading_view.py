from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service.configs.flask_configuration import api
from flask_restful import Resource


class DirectDownloadingView(Resource):
    def get(self, file):
        emit_sending(
            file,
            queue_name=rabbit_configuration.file_queue_name,
            routing_key=rabbit_configuration.file_routing_key
        )

        return 200


api.add_resource(DirectDownloadingView, '/file-download')
