"""View for generation link and downloading file"""
import os
from flask import request, send_file, make_response, jsonify
from flask_api import status
from flask_restful import Resource
from werkzeug.utils import secure_filename
from file_sharing_service.broker.event_handlers import emit_sending
from file_sharing_service.configs import rabbit_configuration
from file_sharing_service import API, APP, DATABASE, UPLOADS_DIR
from file_sharing_service.models.generated_file import GeneratedFile
from file_sharing_service.serializers.generated_file_schema import GeneratedFileSchema
from file_sharing_service.logger.logger import LOGGER
from file_sharing_service import HOST, PORT


ALLOWED_EXTENSIONS = ('csv', 'xls', 'xlsx')


class GeneratedFileLoading(Resource):
    @staticmethod
    def add_to_db(file):
        """
        Function for adding generated file to database
        Args:
            file (GeneratedFile):
        """
        DATABASE.session.add(file)
        DATABASE.session.commit()
        LOGGER.info(f'File {file} was added to the database')

    @staticmethod
    def check_filename(filename):
        old_filename = filename.split('.')[-2]
        for i in range(1000):
            if os.path.exists(os.path.join(APP.config['UPLOAD_FOLDER'], filename)):
                new_filename = f'{old_filename}({i}).{filename.split(".")[-1]}'
                filename = new_filename
            else:
                return filename

    def get(self):
        """
        GET method for check if file already generated

        """
        if 'filter_id' not in request.headers:
            return make_response(
                jsonify({
                    'message': 'NO filter_id in headers'
                }),
                status.HTTP_400_BAD_REQUEST
            )
        elif 'input_file_id' not in request.headers:
            return make_response(
                jsonify({
                    'message': 'NO input_file_id in headers'
                }),
                status.HTTP_400_BAD_REQUEST
            )

        filter_id = request.headers['filter_id']
        input_file_id = request.headers['input_file_id']
        files = GeneratedFile.query.filter_by(filter_id=filter_id, input_file_id=input_file_id).first()

        if files:
            return make_response(
                jsonify({
                    'message': 'Ok',
                    'link': files.file_link
                }),
                status.HTTP_200_OK
            )
        else:
            return make_response(
                jsonify({
                    'message': 'File not generated',
                }),
                status.HTTP_200_OK
            )

    def post(self):
        """
        POST method for adding file to database and generate downloading link

        """

        if 'generated_file' not in request.files:
            return make_response(
                jsonify({
                    'message': 'There is no file in your request'
                }),
                status.HTTP_400_BAD_REQUEST
            )
        elif 'filter_id' not in request.form:
            return make_response(
                jsonify({
                    'message': 'There is no filter_id in your request'
                }),
                status.HTTP_400_BAD_REQUEST
            )
        elif 'input_file_id' not in request.form:
            return make_response(
                jsonify({
                    'message': 'There is no input_file_id in your request'
                }),
                status.HTTP_400_BAD_REQUEST
            )

        generated_file = request.files['generated_file']
        filename = secure_filename(generated_file.filename)

        if not filename.endswith(ALLOWED_EXTENSIONS):
            return make_response(
                jsonify({
                    'message': "File doesn't have allowed extension",
                }),
                status.HTTP_400_BAD_REQUEST
            )

        file_size = os.path.getsize(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
        filter_id = request.form['filter_id']
        input_file_id = request.form['input_file_id']

        filename = GeneratedFileLoading.check_filename(filename)

        generated_file.filename = filename
        generated_file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))

        input_file = GeneratedFile(
            file_name=filename,
            file_link=f'{HOST}:{PORT}/download/{filename}',
            file_size=file_size,
            input_file_id=input_file_id,
            filter_id=filter_id
        )

        schema = GeneratedFileSchema()
        GeneratedFileLoading.add_to_db(input_file)

        data = schema.dump(input_file)
        emit_sending(data, rabbit_configuration.FILE_DELETION_NAME, rabbit_configuration.FILE_DELETION_KEY)

        return make_response(
            jsonify({
                'data': data,
            }),
            status.HTTP_201_CREATED
        )


class GeneratedFileInterface(Resource):
    @staticmethod
    def remove_from_db(file):
        """
        Function for deleting file from database
        Args:
            file:

        """
        DATABASE.session.delete(file)
        DATABASE.session.commit()
        LOGGER.info(f'File {file} was deleted from the database')

    def get(self, generated_file_id):
        """
        GET method for downloading files
        Args:
            generated_file_id:

        Returns:

        """
        try:
            filename = GeneratedFile.query.get(generated_file_id).file_name

            return send_file(UPLOADS_DIR + filename, attachment_filename=filename)
        except AttributeError:
            return make_response(
                jsonify({
                    'message': f'File with id {generated_file_id} not found'
                }),
                status.HTTP_400_BAD_REQUEST
            )

    def delete(self, generated_file_id):
        """
        DELETE method for deleting file from database and storage
        Args:
            generated_file_id:
        """
        generated_file = GeneratedFile.query.get(generated_file_id)
        if generated_file:
            filename = generated_file.file_name
            try:
                os.remove(UPLOADS_DIR + filename)
            except FileNotFoundError:
                return make_response(
                    jsonify({
                        'message': f'File was not found'
                    }),
                    status.HTTP_204_NO_CONTENT
                )

            GeneratedFileInterface.remove_from_db(generated_file)
            return make_response(
                jsonify({
                    'message': f'File with id {generated_file_id} was deleted'
                }),
                status.HTTP_200_OK
            )
        else:
            return make_response(
                jsonify({
                    'message': f'File with id {generated_file_id} not found'
                }),
                status.HTTP_400_BAD_REQUEST
            )


API.add_resource(GeneratedFileInterface, '/download/<int:generated_file_id>')
API.add_resource(GeneratedFileLoading, '/download/')
