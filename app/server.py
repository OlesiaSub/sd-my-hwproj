from datetime import datetime
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.requests import Request

from app.controllers.controller_student import ControllerStudent
from app.controllers.controller_teacher import ControllerTeacher
from app.form.attempt import AttemptCreateForm
from app.form.new_checker import NewCheckerCreateForm
from app.form.new_hw import NewHwCreateForm
from app.logic.database_server import DatabaseServer
from app.models import models

router = InferringRouter()
templates = Jinja2Templates(directory="templates")


@cbv(router)
class Server:
    controllerStudent = ControllerStudent()
    controllerTeacher = ControllerTeacher()
    databaseServer = DatabaseServer()

    @router.get("/student", response_model=List[models.Homework])
    def student(self, request: Request):
        return templates.TemplateResponse("student_hub.html",
                                          {"request": request})

    @router.get("/student/hw")
    def get_student_hw(self, request: Request):
        return templates.TemplateResponse("hw_list.html",
                                          {"request": request, "hws": self.controllerStudent.get_hw_sorted()})

    @router.get("/student/results", response_model=List[models.Result])
    def get_student_results(self, request: Request):
        return templates.TemplateResponse("result_list.html",
                                          {"request": request, "results": self.controllerStudent.get_results_sorted()})

    @router.get("/student/results/{id}", response_model=models.Result)
    def get_student_result_by_id(self, request: Request, id: int):
        return templates.TemplateResponse("hw_result.html",
                                          {"request": request, "result": self.controllerStudent.get_result_by_id(id)})

    @router.get("/student/hw/{id}/submit")
    def create_attempt(self, request: Request, id: int):
        return templates.TemplateResponse("create_attempt.html", {"request": request})

    @router.post("/student/hw/{id}/submit", response_model=models.Result)
    async def submit_hw(self, id: int, request: Request):
        form = AttemptCreateForm(request)
        await form.load_data()
        if form.is_valid():
            attempt = models.Attempt(solution=form.solution)
            self.controllerStudent.submit_hw(id, attempt)
        return templates.TemplateResponse("create_attempt.html", form.__dict__)

    @router.get("/teacher/results", response_model=List[models.Result])
    def get_teacher_results(self, request: Request):
        return templates.TemplateResponse("teacher_result_list.html",
                                          {"request": request, "results": self.controllerTeacher.get_results_sorted()})

    @router.get("/teacher/new_homework")
    def hw_get(self, request: Request):
        return templates.TemplateResponse('new_hw.html', context={'request': request})

    @router.post("/teacher/new_homework")
    async def hw_post(self, request: Request):
        form = NewHwCreateForm(request)
        await form.load_data()
        deadline = form.deadline.replace('-', '/')
        date_time_deadline = datetime.strptime(deadline[2:], '%y/%m/%d')
        date = datetime.now()
        date = date.replace(day=date.day - 1)
        hw = models.Homework(full_name=form.name, task_text=form.text, deadline=date_time_deadline,
                             publication_date=date)
        self.controllerTeacher.add_hw(homework=hw)
        return templates.TemplateResponse("new_hw.html", form.__dict__)

    # @router.get("/teacher/new_script")
    # def checker_get(self, request: Request):
    #     return templates.TemplateResponse('new_checker.html', context={'request': request})
    #
    # @router.post("/teacher/new_script")
    # async def hw_post(self, request: Request):
    #     form = NewCheckerCreateForm(request)
    #     await form.load_data()
    #     checker = models.Checker(name=form.name, script=form.script)
    #     self.controllerTeacher.update_checker(checker=checker)
    #     return templates.TemplateResponse("new_checker.html", form.__dict__)


server = Server()
app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
