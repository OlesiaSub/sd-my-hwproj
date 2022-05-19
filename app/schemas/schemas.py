from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from app.logic.database_server import Base


class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True, index=True)
    publication_date = Column(DateTime(timezone=True), default=now())
    task_text = Column(String)
    deadline = Column(DateTime(timezone=True))


class Attempt(Base):
    __tablename__ = "attempt"

    id = Column(Integer, primary_key=True)
    homework_id = Column(Integer)
    solution = Column(String)


class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True)
    data = Column(DateTime(timezone=True))
    attempt_id = Column(Integer)
    mark = Column(Integer)
    comment = Column(String)
