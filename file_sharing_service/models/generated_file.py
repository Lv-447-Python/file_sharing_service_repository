"""Model for file_sharing_service"""

import datetime
from file_sharing_service import DATABASE


class GeneratedFile(DATABASE.Model):
    __tablename__ = 'generated_files'

    file_name = DATABASE.Column(DATABASE.String, primary_key=True, unique=True, nullable=False)
    file_datetime = DATABASE.Column(DATABASE.DateTime, nullable=False, default=datetime.datetime.now())
    file_link = DATABASE.Column(DATABASE.VARCHAR, nullable=False)
    file_size = DATABASE.Column(DATABASE.INTEGER, nullable=False)
    input_file_id = DATABASE.Column(DATABASE.INTEGER, nullable=False)
    filter_id = DATABASE.Column(DATABASE.INTEGER, nullable=False)

    def __init__(self, file_name, file_link, file_size, input_file_id, filter_id):
        self.file_name = file_name
        self.file_link = file_link
        self.file_datetime = datetime.datetime.now()
        self.file_size = file_size
        self.input_file_id = input_file_id
        self.filter_id = filter_id

