from sqlalchemy.sql.functions import now

from app.logic.database_server import Base, engine
from app.logic import database_server
from app.models.models import Attempt
from app.schemas import schemas
from app.logic.task_queue import TaskQueue


class ControllerStudent:
    databaseServer = database_server.DatabaseServer()
    Base.metadata.create_all(bind=engine)
    queue = TaskQueue()

    def get_hw_sorted(self):
        db = next(self.databaseServer.get_db())
        hws = db.query(schemas.Homework).filter(schemas.Homework.publication_date <= now()) \
            .order_by(schemas.Homework.deadline).all()
        return hws

    def get_results_sorted(self):
        db = next(self.databaseServer.get_db())
        results = db.query(schemas.Result).order_by(schemas.Result.date).all()
        return list(map(lambda x: schemas.Result(id=x.id, comment=x.comment, mark=x.mark, date=x.date), results))

    def submit_hw(self, hw_id, attempt: Attempt):
        db = next(self.databaseServer.get_db())
        db_attempt = schemas.Attempt(homework_id=hw_id, solution=attempt.solution)
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)

        message = dict({
            'attempt_id': db_attempt.id,
            'homework_id': hw_id,
            'date': now(),
            #'solution': 'https://raw.githubusercontent.com/OlesiaSub/sd-my-hwproj/impl-1/app/server.py',
             'solution': db_attempt.solution,
            'checker': 'https://raw.githubusercontent.com/OlesiaSub/sd-my-hwproj/impl-1/app/schemas/schemas.py'})

        self.queue.push_message(message)

        return None

    def get_result_by_id(self, result_id: int):
        db = next(self.databaseServer.get_db())
        return db.query(schemas.Result).filter(schemas.Result.id == result_id).first()

