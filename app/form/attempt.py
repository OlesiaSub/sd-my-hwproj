from typing import List

from fastapi import Request


class AttemptCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.solution: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.solution = form.get("solution")

    def is_valid(self):
        # if not self.title or not len(self.title) >= 4:
        #     self.errors.append("A valid title is required")
        # if not self.company_url or not (self.company_url.__contains__("http")):
        #     self.errors.append("Valid Url is required e.g. https://example.com")
        # if not self.company or not len(self.company) >= 1:
        #     self.errors.append("A valid company is required")
        # if not self.description or not len(self.description) >= 20:
        #     self.errors.append("Description too short")
        # if not self.errors:
        #     return True
        return True
