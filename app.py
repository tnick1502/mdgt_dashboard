from fastapi import FastAPI
from api import router

app = FastAPI(
    title="DashBoard MDGT",
    description="Отображение показателей работы компании",
    version="1.0.0"
)

app.include_router(router)