"""Model for file_sharing_service"""

import datetime
import sqlalchemy
from file_sharing_service import database


class GeneratedFile(database.Model):
    __tablename__ = 'generated_files'

    id = sqlalchemy.Column(database.INTEGER, primary_key=True, autoincrement=True)
    file_name = sqlalchemy.Column(database.String(100), unique=True, nullable=False)
    file_path = sqlalchemy.Column(database.Text, unique=True, nullable=False)
    file_datetime = sqlalchemy.Column(database.DateTime, nullable=False, default=datetime.datetime.now())
