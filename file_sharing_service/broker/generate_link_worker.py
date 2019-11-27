"""File for downloading link generation"""
import requests


def get_filepath(user_id, filter_id, file_id):
    api_call = f'http://localhost:5000/generate?file_id={file_id}&filter_id={filter_id}&user_id={user_id}'
    response = requests.get(api_call)

    json_response = response.json()
    filepath = json_response['filepath']
    return filepath


def generate_downloading_link(filepath):
    print(f'127.0.0.1:5000/download?filepath={filepath}')
    return f'127.0.0.1/download/{filepath}'


def send_file(file_data):
    filepath = get_filepath(file_data['user_id'], file_data['filter_id'], file_data['file_id'])
    downloading_link = generate_downloading_link(filepath)
    return downloading_link
