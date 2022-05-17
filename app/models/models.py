import datetime
from typing import Optional

from pydantic.main import BaseModel


class Homework(BaseModel):
    full_name: str
    task_text: Optional[str] = None
    deadline: datetime.datetime


class Attempt(BaseModel):
    solution: str


class Result(BaseModel):
    comment: str
    mark: int
