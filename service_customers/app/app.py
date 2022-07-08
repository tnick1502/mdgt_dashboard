from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import router
from background_tasks import update_db
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
    array.append(f"http://{ip}")
    for port in ports:
        array.append(f"http://{ip}:{str(port)}")
    return array

app = FastAPI(
    title="DashBoard MDGT",
    description="Отображение показателей работы компании",
    version="1.0.0",
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://192.168.0.200",
    "http://192.168.0.200:80",
    "http://192.168.0.200:3000",
    "http://192.168.0.41:3000",
    "http://192.168.0.41",
    "http://localhost"]

origins += get_self_public_ip()

origins += create_ip_ports_array(get_self_public_ip(), 3000, 9600, 80)


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
    update_db()
