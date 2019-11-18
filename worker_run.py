from file_sharing_service.broker.workers import email_sending_worker
import sys


if __name__ == '__main__':
    queue = sys.argv[1]
    route = sys.argv[2]
    # email_sending_worker('email_queue', 'email_sending')
    email_sending_worker(queue, route)
