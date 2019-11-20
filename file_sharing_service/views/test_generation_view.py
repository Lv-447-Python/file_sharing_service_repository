from file_sharing_service.configs.flask_configuration import api
from flask_restful import Resource


class GenerateFileView(Resource):
    def get(self):
        response = {
            'status': 200,
            'msg': 'Success',
            'filepath': '/home/andrew/file_sharing_service_repository/homes.csv'
            }
        return response


api.add_resource(GenerateFileView, '/generate')
