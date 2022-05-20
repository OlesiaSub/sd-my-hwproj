from sqlalchemy.sql.functions import now

from app.logic.database_server import Base, engine
from app.models import models
from app.logic import database_server
from app.models.models import Attempt
from app.schemas import schemas


class ControllerStudent:
    databaseServer = database_server.DatabaseServer()
    Base.metadata.create_all(bind=engine)

    def get_hw_sorted(self):
        db = next(self.databaseServer.get_db())
        hws = db.query(schemas.Homework).filter(schemas.Homework.publication_date <= now()) \
            .order_by(schemas.Homework.deadline).all()
        return list(
            map(lambda x: models.Homework(full_name=x.full_name, task_text=x.task_text, deadline=x.deadline,
                                          publication_date=x.publication_date), hws))

    def get_results_sorted(self):
        db = next(self.databaseServer.get_db())
        results = db.query(schemas.Result).order_by(schemas.Result.data).all()
        return list(map(lambda x: models.Result(comment=x.comment, mark=x.mark, data=x.data), results))

    def submit_hw(self, hw_id, attempt: Attempt):
        db = next(self.databaseServer.get_db())
        db_attempt = schemas.Attempt(homework_id=hw_id,
                                     solution=attempt.solution)
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        result = schemas.Result(data=now(), attempt_id=db_attempt.id, mark=5, comment="good")
        db.add(result)
        db.commit()
        db.refresh(result)
        return models.Result(comment=result.comment, mark=result.mark, data=result.data)
