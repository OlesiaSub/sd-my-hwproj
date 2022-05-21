import pika
import json

from app.logic import database_server
from app.logic.runner import Runner
from app.schemas import schemas
from sqlalchemy.sql.functions import now

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
runner = Runner()

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    task = json.loads(body)
    print(" [x] Received %r" % task)
    res = runner.run_task(task)

    databaseServer = database_server.DatabaseServer()
    db = next(databaseServer.get_db())
    result = schemas.Result(date=now(), attempt_id=task.attempt_id, mark=res[0], comment=res[1])
    db.add(result)
    db.commit()
    db.refresh(result)

    print(" [x] Done:", res)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
