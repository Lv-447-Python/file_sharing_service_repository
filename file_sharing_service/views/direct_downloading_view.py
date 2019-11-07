from flask import send_file
from file_sharing_service.configs.flask_configuration import api
from flask_restful import Resource


class DirectDownloadingView(Resource):
    def get(self):
        return send_file('homes.csv')


api.add_resource(DirectDownloadingView, '/file-download')
