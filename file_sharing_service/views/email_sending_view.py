"""View for sending email with file"""
from flask import request, make_response, jsonify
from flask_api import status
from flask_restful import Resource
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service import API
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service.models.generated_file import GeneratedFile
from file_sharing_service.serializers.generated_file_schema import GeneratedFileSchema
import ast


class EmailSendingView(Resource):
    def get(self, generated_file_name):
        """
        GET method for sending email with attached file

        """

        generated_file = GeneratedFile.query.get(generated_file_name)
        schema = GeneratedFileSchema()
        generated_file_json = schema.dump(generated_file)

        if not generated_file:
            return make_response(
                jsonify({
                    'message': f'File was not found'
                }),
                status.HTTP_204_NO_CONTENT
            )

        email_args = request.args['email']
        email_args = ast.literal_eval(email_args)

        file_data = {
            'file': generated_file_json,
            'email': email_args
        }

        emit_sending(
            file_data,
            queue_name=rabbit_configuration.EMAIL_QUEUE_NAME,
            routing_key=rabbit_configuration.EMAIL_ROUTING_KEY
        )

        return make_response(
            jsonify({
                'message': 'Message was sent to the queue ' + rabbit_configuration.EMAIL_QUEUE_NAME
            }),
            status.HTTP_200_OK
        )


API.add_resource(EmailSendingView, '/email/<string:generated_file_name>/')
