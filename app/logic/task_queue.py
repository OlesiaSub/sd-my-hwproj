import pika
import json

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5671

class TaskQueue:
    def push_message(self, message):
        with pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST)) as connection:
            channel = connection.channel()
            channel.queue_declare(queue='task_queue', durable=True)

            channel.basic_publish(
                exchange='',
                routing_key='task_queue',
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
