"""Model for file_sharing_service"""

import datetime
import sqlalchemy
from file_sharing_service import DATABASE


class GeneratedFile(DATABASE.Model):
    __tablename__ = 'generated_files'

    id = sqlalchemy.Column(DATABASE.INTEGER, primary_key=True, autoincrement=True)
    file_name = sqlalchemy.Column(DATABASE.String(100), unique=True, nullable=False)
    file_path = sqlalchemy.Column(DATABASE.Text, unique=True, nullable=False)
    file_datetime = sqlalchemy.Column(DATABASE.DateTime, nullable=False, default=datetime.datetime.now())
