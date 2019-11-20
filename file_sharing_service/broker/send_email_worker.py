from file_sharing_service.configs import smtp_configuration
from .generate_link_worker import get_filepath
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(file_data):
    subject = 'FilterMe File'
    body = '''This email was sent by FilterMe. Your file was successfully generated.'''

    message = MIMEMultipart()
    message['From'] = smtp_configuration.sender_email
    message['To'] = file_data['email']
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    filename = get_filepath(file_data['user_id'],
                            file_data['filter_id'],
                            file_data['file_id'])

    try:
        with open(filename, 'rb') as attachment:
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
    with smtplib.SMTP_SSL('smtp.gmail.com', port=smtp_configuration.port, context=context) as server:
        server.login(smtp_configuration.sender_email, smtp_configuration.sender_password)
        server.sendmail(smtp_configuration.sender_email, smtp_configuration.receiver_email, text)
