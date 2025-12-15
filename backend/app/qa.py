from fastapi import FastAPI

from app.routers.qa import router


def run_qa(app: FastAPI):
    app.include_router(router)
