from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session

from app.models import models
from app.logic import utils, database

router = APIRouter()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/teacher/hw/add", response_model=models.Homework)
def create_new_hw(homework: models.Homework, db: Session = Depends(get_db)):
    hw_db = utils.get_hw_by_name(db, name=homework.full_name)
    if hw_db:
        raise HTTPException(status_code=400, detail="Homework with such name already exist")
    homework = utils.create_hw(db=db, homework=homework)
    db.commit()
    db.refresh(homework)
    return models.Homework(full_name=homework.full_name, task_text=homework.task_text, deadline=homework.deadline)


@router.get("/teacher/hw", response_model=List[models.Homework])
def get_hws(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hws = list(map(lambda x: models.Homework(full_name=x.full_name, task_text=x.task_text, deadline=x.deadline),
                           utils.get_hws(db, skip=skip, limit=limit)))
    return hws
