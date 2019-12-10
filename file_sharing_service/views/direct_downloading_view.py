"""View for generation link and downloading file"""
import os
from flask import request, send_file, make_response, jsonify
from flask_api import status
from flask_restful import Resource
from werkzeug.utils import secure_filename
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service import API, APP, DATABASE, HOST, PORT, UPLOADS_DIR
from file_sharing_service.models.generated_file import GeneratedFile
from file_sharing_service.serializers.generated_file_schema import GeneratedFileSchema


ALLOWED_EXTENSIONS = ('csv', 'xls', 'xlsx')


class GeneratedFileLoading(Resource):
    @staticmethod
    def generate_link(id):
        """
        Function for generating downloading link
        Args:
            filepath (link):

        Returns:
            downloading link (str)

        """
        return f'{HOST}:{PORT}/download/{id}'

    @staticmethod
    def add_to_db(file):
        """
        Function for adding generated file to database
        Args:
            file (GeneratedFile):
        """
        DATABASE.session.add(file)
        DATABASE.session.commit()

    def post(self):
        """
        POST method for adding file to database and generate downloading link

        """
        if 'generated_file' not in request.files:
            return make_response(jsonify({
                'message': 'There is no file in your request'
            }),
                status.HTTP_400_BAD_REQUEST)

        generated_file = request.files['generated_file']
        filename = secure_filename(generated_file.filename)

        if not filename.endswith(ALLOWED_EXTENSIONS):
            return make_response(jsonify({
                'message': "File doesn't have allowed extension"
            }),
                status.HTTP_400_BAD_REQUEST)

        file_path = UPLOADS_DIR + filename
        file_link = GeneratedFileLoading.generate_link(file_path)
        generated_file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))

        input_file = GeneratedFile(filename, file_path, file_link)

        schema = GeneratedFileSchema()
        GeneratedFileLoading.add_to_db(input_file)

        data = schema.dump(input_file)
        emit_sending(data, rabbit_configuration.FILE_DELETION_NAME, rabbit_configuration.FILE_DELETION_KEY)

        return make_response(
            jsonify({
                'data': data,
            }),
            status.HTTP_201_CREATED)


class GeneratedFileInterface(Resource):
    @staticmethod
    def remove_from_db(file):
        DATABASE.session.delete(file)
        DATABASE.session.commit()

    def get(self, generated_file_id):
        try:
            filename = GeneratedFile.query.get(generated_file_id).file_name

            return send_file(UPLOADS_DIR + filename)
        except AttributeError:
            return make_response(
                jsonify({
                    'message': f'File with id {generated_file_id} not found'
                }),
                status.HTTP_400_BAD_REQUEST
            )

    def delete(self, generated_file_id):
        generated_file = GeneratedFile.query.get(generated_file_id)
        if generated_file:
            filename = generated_file.file_name
            try:
                os.remove(UPLOADS_DIR + filename)
            except FileNotFoundError:
                print('File not found')

            GeneratedFileInterface.remove_from_db(generated_file)
            return make_response(
                jsonify({
                    'message': 'Success'
                }),
                status.HTTP_200_OK)
        else:
            return make_response(
                jsonify({
                    'message': f'File with id {generated_file_id} not found'
                }),
                status.HTTP_400_BAD_REQUEST
            )


API.add_resource(GeneratedFileInterface, '/download/<int:generated_file_id>')
API.add_resource(GeneratedFileLoading, '/download/')
