"""Test GenerateFileView"""
from flask_restful import Resource
from file_sharing_service import API


class GenerateFileView(Resource):
    def get(self):
        response = {
            'status': 200,
            'msg': 'Success',
            'filepath': '/home/andrew/file_sharing_service_repository/homes.csv'
            }
        return response


API.add_resource(GenerateFileView, '/generate')
