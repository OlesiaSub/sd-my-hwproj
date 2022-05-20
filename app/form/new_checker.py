import datetime
from typing import List

from fastapi import Request


class NewCheckerCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: str = ""
        self.script: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.script = form.get("script")

    # todo validation
