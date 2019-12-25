"""The main worker file """
import ast
import pika
from file_sharing_service.broker.send_email_worker import send_email
from file_sharing_service.broker.delete_timer_worker import deletion_timer
from file_sharing_service.logger.logger import LOGGER


def callback(ch, method, properties, body):
    file_data_decoded = body.decode('utf-8')
    file_data = ast.literal_eval(file_data_decoded)

    if method.routing_key == 'email_sending':
        print(f'Message {file_data}. Routing key: {method.routing_key}')
        send_email(file_data)
    elif method.routing_key == 'file_deletion_key':
        print(f'Message {file_data}. Routing key: {method.routing_key}')
        deletion_timer(file_data)
    else:
        print('Invalid routing key')

    return method.routing_key


def manage_jobs(queue_name, binding_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # credentials = pika.PlainCredentials('admin', 'admin')
    # connection = pika.BlockingConnection(pika.ConnectionParameters(
    #     '0.0.0.0',
    #     5677,
    #     '/',
    #     credentials
    # ))

    channel = connection.channel()

    exchange_name = 'exchange_files'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct',
        durable=True
    )

    queue_choose = channel.queue_declare(queue=queue_name)
    queue_chosen = queue_choose.method.queue

    channel.queue_bind(exchange=exchange_name,
                       queue=queue_chosen,
                       routing_key=bytes(binding_key, encoding='UTF-8'))

    LOGGER.info('[*] Waiting for messages')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()
