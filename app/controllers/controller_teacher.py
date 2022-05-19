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

    def add_hw(self):
        pass

    def update_checker(self):
        pass
