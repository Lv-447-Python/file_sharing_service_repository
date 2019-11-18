import pika
from file_sharing_service.broker.send_email_worker import send_email


def manage_jobs(queue_name, binding_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'exchange_files'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct',
        durable=True
    )

    queue_email = channel.queue_declare(queue=queue_name)
    queue_email_name = queue_email.method.queue

    channel.queue_bind(exchange=exchange_name,
                       queue=queue_email_name,
                       routing_key=bytes(binding_key, encoding='UTF-8'))

    print('[*] Waiting for messages')

    def callback(ch, method, properties, body):
        if method.routing_key == 'email_sending':
            send_email(str(body))
        elif method.routing_key == 'files_sending':
            print('file sent')
        else:
            print('Invalid routing key')

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()
