from file_sharing_service.configs import smtp_configuration
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .generate_link_worker import get_filepath
import ast


def parse_file_data(bytes_data):
    file_data_decoded = bytes_data.decode('utf-8')
    file_data_dict = ast.literal_eval(file_data_decoded)
    user_id = int(file_data_dict['user_id'])
    filter_id = int(file_data_dict['filter_id'])
    file_id = int(file_data_dict['file_id'])

    file_data = {
        'user_id': user_id,
        'filter_id': filter_id,
        'file_id': file_id
    }

    return file_data


def send_email(file_data):
    subject = 'FilterMe File'
    body = '''This email was sent by FilterMe. Your file was successfully generated.'''

    message = MIMEMultipart()
    message['From'] = smtp_configuration.sender_email
    message['To'] = smtp_configuration.receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    params_to_get_filename = parse_file_data(file_data)

    filename = get_filepath(params_to_get_filename['user_id'],
                            params_to_get_filename['filter_id'],
                            params_to_get_filename['file_id'])

    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header('Content-Disposition', f'attachment; filename={filename}')

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port=smtp_configuration.port, context=context) as server:
        server.login(smtp_configuration.sender_email, smtp_configuration.sender_password)
        server.sendmail(smtp_configuration.sender_email, smtp_configuration.receiver_email, text)

    print('Email was sent')
