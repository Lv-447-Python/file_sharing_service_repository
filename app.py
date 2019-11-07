from file_sharing_service.configs.flask_configuration import app
from file_sharing_service.views.direct_downloading_view import DirectDownloadingView
from file_sharing_service.views.email_sending_view import EmailSendingView


if __name__ == '__main__':
    app.run()
