"""File for downloading link generation"""
import datetime
import time
import requests


def deletion_timer(file_data):
    """
    Function for automatic deletion files
    Args:
        file_data:

    Returns:

    """
    creation_time = datetime.datetime.strptime(file_data['file_datetime'], '%Y-%m-%dT%H:%M:%S.%f')
    deletion_time = creation_time + datetime.timedelta(seconds=100)
    file_id = file_data['id']

    try:
        time.sleep((deletion_time - datetime.datetime.now()).total_seconds())
        response = requests.delete(f'http://127.0.0.1:5000/download/{file_id}')
        print('API call for deletion was sent')
        print(f'Response: {response.json()}')
    except ValueError:
        print('API call for deletion was not sent, Value Error')
