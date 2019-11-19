from file_sharing_service.configs.flask_configuration import app
from file_sharing_service.views.direct_downloading_view import DirectDownloadingView
from file_sharing_service.views.direct_downloading_view import DownloadingLinkView
from file_sharing_service.views.email_sending_view import EmailSendingView
from file_sharing_service.views.test_generation_view import GenerateFileView


if __name__ == '__main__':
    app.run()
