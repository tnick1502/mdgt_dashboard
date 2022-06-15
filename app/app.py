from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import router
from background_tasks import create_admin, update_db
from db.tables import Base
import http
from db.database import engine
from settings import settings
from fastapi.templating import Jinja2Templates

def get_self_public_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode()

def create_ip_ports_array(ip: str, *ports):
    array = []
    for port in ports:
        array.append(f"{ip}:{str(port)}")
    return array


app = FastAPI(
    title="Georeport MDGT",
    description="Сервис аутентификации протоколов испытаний",
    version="1.0.0")


app = FastAPI(
    title="DashBoard MDGT",
    description="Отображение показателей работы компании",
    version="1.0.0",
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)


origins = [
    "http://localhost:3000",
    "http://localhost:8080"]

origins += create_ip_ports_array(get_self_public_ip(), 3000, 8000, 80)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers",
                   'Content-Type',
                   'Authorization',
                   'Access-Control-Allow-Origin'])

app.include_router(router)

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(engine)
    create_admin()
    update_db(settings.prize_directory, settings.statment_excel_path)
