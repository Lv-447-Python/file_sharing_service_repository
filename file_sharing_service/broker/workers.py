"""The main worker file """
import ast
import pika
from file_sharing_service.broker.send_email_worker import send_email
from file_sharing_service.broker.delete_timer_worker import deletion_timer


def parse_file_data(bytes_data):
    file_data_decoded = bytes_data.decode('utf-8')
    file_data_dict = ast.literal_eval(file_data_decoded)

    return file_data_dict


def callback(ch, method, properties, body):
    try:
        file_data = parse_file_data(body)
    except KeyError:
        print('No email in file data')
        return None

    if method.routing_key == 'email_sending':
        send_email(file_data)
        print('Email sent')
    elif method.routing_key == 'file_deletion_key':
        deletion_timer(file_data)
    else:
        print('Invalid routing key')

    return method.routing_key


def manage_jobs(queue_name, binding_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'exchange_files'

    queue_choose = channel.queue_declare(queue=queue_name)
    queue_chosen = queue_choose.method.queue

    channel.queue_bind(exchange=exchange_name,
                       queue=queue_chosen,
                       routing_key=bytes(binding_key, encoding='UTF-8'))

    print('[*] Waiting for messages')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()
