from sqlalchemy.orm.session import Session

from app.schemas import schemas
from app.models import models


def get_hw(db: Session, internship_id: int):
    return db.query(schemas.Homework).filter(schemas.Homework.id == internship_id).first()


def get_hw_by_name(db: Session, name: str):
    return db.query(schemas.Homework).filter(schemas.Homework.full_name == name).first()


def get_hws(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Homework).offset(skip).limit(limit).all()


def create_hw(db: Session, homework: models.Homework):
    db_hw = schemas.Homework(full_name=homework.full_name, task_text=homework.task_text,
                                     deadline=homework.deadline)
    db.add(db_hw)
    return db_hw
