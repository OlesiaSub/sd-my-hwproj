import datetime
from typing import List

from fastapi import Request


class NewHwCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: str = ""
        self.text: str = ""
        self.deadline: str = "no deadline"
        self.publication_date: datetime.datetime = datetime.datetime.now()

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.text = form.get("text")
        self.deadline = form.get("deadline")

    # todo validation
