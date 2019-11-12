import pika


def emit_sending(file, queue_name, routing_key):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'exchange_files'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct',
        durable=True
    )

    channel.queue_declare(queue=queue_name)
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=file,

        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print(f'{routing_key} sent to {exchange_name} with message {file}')
    connection.close()
