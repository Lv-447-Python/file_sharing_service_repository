from file_sharing_service import APP, HOST, PORT
from file_sharing_service.views.direct_downloading_view import GeneratedFileLoading, GeneratedFileInterface
from file_sharing_service.views.email_sending_view import EmailSendingView
from file_sharing_service.views.generated_files_view import GeneratedFileView


if __name__ == '__main__':
    APP.run(host=HOST, port=PORT)
