"""Model for file_sharing_service"""

import datetime
import sqlalchemy
from file_sharing_service import DATABASE


class GeneratedFile(DATABASE.Model):
    __tablename__ = 'generated_files'

    id = DATABASE.Column(DATABASE.INTEGER, primary_key=True, autoincrement=True)
    file_name = DATABASE.Column(DATABASE.String(100), unique=True, nullable=False)
    file_datetime = DATABASE.Column(DATABASE.DateTime, nullable=False, default=datetime.datetime.now)
    file_link = DATABASE.Column(DATABASE.VARCHAR, nullable=False)
    file_size = DATABASE.Column(DATABASE.INTEGER, nullable=False)

    def __init__(self, file_name, file_link, file_size):
        self.file_name = file_name
        self.file_link = file_link
        self.file_datetime = datetime.datetime.now()
        self.file_size = file_size

    def __repr__(self):
        return f'\t File: {self.file_name}'
