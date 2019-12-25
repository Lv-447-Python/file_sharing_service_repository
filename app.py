from file_sharing_service import APP, HOST, PORT
from file_sharing_service.views.direct_downloading_view import GeneratedFileLoading, GeneratedFileInterface
from file_sharing_service.views.email_sending_view import EmailSendingView


if __name__ == '__main__':
    APP.run(host='0.0.0.0')
