from file_sharing_service.broker.workers import manage_jobs
import sys


if __name__ == '__main__':
    queue = sys.argv[1]
    route = sys.argv[2]
    manage_jobs(queue, route)
