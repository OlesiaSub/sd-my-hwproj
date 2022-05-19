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
        db = self.databaseServer.get_db()
        hws = next(db).query(schemas.Homework).filter(schemas.Homework.publication_date <= now()) \
            .order_by(schemas.Homework.deadline).all()
        return list(
            map(lambda x: models.Homework(full_name=x.full_name, task_text=x.task_text, deadline=x.deadline,
                                          publication_date=x.publication_date), hws))

    def get_results_sorted(self):
        db = self.databaseServer.get_db()
        results = next(db).query(schemas.Result).order_by(schemas.Result.data).all()
        return list(map(lambda x: models.Result(comment=x.comment, mark=x.mark, data=x.data), results))

    def submit_hw(self, hw_id, attempt: Attempt):
        pass
