from typing import List
from fastapi import FastAPI, Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.controllers.controller_student import ControllerStudent
from app.controllers.controller_teacher import ControllerTeacher
from app.models import models
from app.models.models import Attempt
from app.logic.database_server import DatabaseServer

router = InferringRouter()
templates = Jinja2Templates(directory="templates")


@cbv(router)
class Server:
    controllerStudent = ControllerStudent()
    controllerTeacher = ControllerTeacher()
    databaseServer = DatabaseServer()

    @router.get("/student/hw", response_model=List[models.Homework])
    def get_hw(self, request: Request):
        return templates.TemplateResponse("hw_list.html",
                                          {"request": request, "hws": self.controllerStudent.get_hw_sorted()})

    @router.get("/student/result", response_model=List[models.Result])
    def get_result(self, request: Request):
        return templates.TemplateResponse("result_list.html",
                                          {"request": request, "results": self.controllerStudent.get_results_sorted()})

    @router.post("/student/hw/{id}", response_model=List[models.Result])
    def submit_hw(self, attempt: Attempt, id: int):
        return self.controllerStudent.submit_hw(id, attempt)

    @router.post("/teacher/new_homework")
    def add_homework(self, homework: models.Homework, db: Session = Depends(databaseServer.get_db)):
        return self.controllerTeacher.create_hw(homework, db)


server = Server()
app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
