import datetime
from typing import Optional

from pydantic.main import BaseModel


class Homework(BaseModel):
    full_name: str
    task_text: Optional[str] = None
    deadline: datetime.datetime
    publication_date: datetime.datetime


class Attempt(BaseModel):
    solution: str


class Result(BaseModel):
    id: int
    comment: str
    mark: int
    date: datetime.datetime
    # checker_output: str # todo


class Checker(BaseModel):
    name: str
    script: str
