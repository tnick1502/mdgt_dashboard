from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import router
from background_tasks import create_admin, update_db
from db.tables import Base
from db.database import engine
from settings import settings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="DashBoard MDGT",
    description="Отображение показателей работы компании",
    version="1.0.0")


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://192.168.0.41:3000/"
    "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


app.include_router(router)

#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(engine)
    create_admin()
    update_db(settings.prize_directory, settings.statment_excel_path)
