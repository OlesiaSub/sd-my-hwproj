from app.logic.task_queue import TaskQueue

queue = TaskQueue()

message = dict({
    'id': 12345,
    'homework_id': 1,
    'solution': 'https://raw.githubusercontent.com/OlesiaSub/sd-my-hwproj/impl-1/app/server.py',
    'checker': 'https://raw.githubusercontent.com/OlesiaSub/sd-my-hwproj/impl-1/app/schemas/schemas.py'})

queue.push_message(message)
