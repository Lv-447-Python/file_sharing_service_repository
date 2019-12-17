"""Script that sends email with file"""
import smtplib
import ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from file_sharing_service.configs import smtp_configuration
from file_sharing_service import APP


def send_email(file_data):
    """
    Function for sending emails with attached files
    Args:
        file_data:


    """
    subject = 'FilterMe File'
    body = '''This email was sent by FilterMe. Your file was successfully generated.'''

    message = MIMEMultipart()
    message['From'] = smtp_configuration.SENDER_EMAIL
    message['To'] = file_data['email']
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    receiver_email = file_data['email']

    filename = file_data['filename']

    file_sharing_dir = os.path.dirname(APP.root_path)
    uploads_dir = os.path.join(file_sharing_dir, APP.config['UPLOAD_FOLDER'])
    filepath = uploads_dir + filename

    try:
        with open(filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

    except FileNotFoundError:
        print('File not found')
        return None

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port=smtp_configuration.PORT, context=context) as server:
        server.login(smtp_configuration.SENDER_EMAIL, smtp_configuration.SENDER_PASSWORD)
        server.sendmail(smtp_configuration.SENDER_EMAIL, receiver_email, text)

    print(f'Email with attached file {filename} was sent to {receiver_email}')

    if filename.endswith('zip'):
        os.remove(filename)
        print('file has been removed')
