from sqlalchemy.orm import Session

from app.logic import database_server
from app.logic.database_server import Base, engine
from app.models import models
from app.schemas import schemas


class ControllerTeacher:
    databaseServer = database_server.DatabaseServer()
    Base.metadata.create_all(bind=engine)

    def get_results_sorted(self):
        db = self.databaseServer.get_db()
        results = next(db).query(schemas.Result).order_by(schemas.Result.data).all()
        return list(map(lambda x: models.Result(comment=x.comment, mark=x.mark, data=x.data), results))

    def add_hw(self, homework: models.Homework):
        db = next(self.databaseServer.get_db())
        db_homework = schemas.Homework(full_name=homework.full_name,
                                       deadline=homework.deadline,
                                       publication_date=homework.publication_date,
                                       task_text=homework.task_text)
        db.add(db_homework)
        db.commit()
        db.refresh(db_homework)

    # def update_checker(self, checker: models.Checker):
    #     db = next(self.databaseServer.get_db())
    #     db_checker = schemas.Checker(name=checker.name, script=checker.script)
    #     db.add(db_checker)
    #     db.commit()
    #     db.refresh(db_checker)
