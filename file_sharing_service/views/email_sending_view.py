from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs.flask_configuration import api
from file_sharing_service.configs import rabbit_configuration
from flask_restful import Resource


class EmailSendingView(Resource):
    def get(self, file):
        emit_sending(
            file,
            queue_name=rabbit_configuration.email_queue_name,
            routing_key=rabbit_configuration.email_routing_key
        )

        return 200


api.add_resource(EmailSendingView, '/email/<string:file>')
