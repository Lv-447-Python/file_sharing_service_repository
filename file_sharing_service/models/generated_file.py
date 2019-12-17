"""Model for file_sharing_service"""

import datetime
import sqlalchemy
from file_sharing_service import DATABASE


class GeneratedFile(DATABASE.Model):
    __tablename__ = 'generated_files'

    id = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True, autoincrement=True)
    file_name = sqlalchemy.Column(sqlalchemy.String(100), unique=True, nullable=False)
    file_datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now())
    file_link = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)

    def __init__(self, file_name, file_link):
        self.file_name = file_name
        self.file_link = file_link
        self.file_datetime = datetime.datetime.now()
