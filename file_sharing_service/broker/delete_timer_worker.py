"""File for downloading link generation"""
import datetime
import time
import requests
from file_sharing_service import HOST, PORT


def deletion_timer(file_data):
    creation_time = datetime.datetime.strptime(file_data['file_datetime'], '%Y-%m-%dT%H:%M:%S.%f')
    deletion_time = creation_time + datetime.timedelta(seconds=10)
    file_id = file_data['id']

    try:
        time.sleep((deletion_time - datetime.datetime.now()).total_seconds())
        requests.delete(f'http://{HOST}:{PORT}/download/{file_id}')
        print('API call for deletion was sent')
    except ValueError:
        print('API call for deletion was not sent, Value Error')
