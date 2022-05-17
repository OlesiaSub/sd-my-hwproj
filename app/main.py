from fastapi import FastAPI

from app.controllers import routers

app = FastAPI()
app.include_router(routers.router)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
