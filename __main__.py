import uvicorn
from settings import settings
from app import app
from services.statment import Statment

Statment(settings.statment_excel_path)

uvicorn.run(
    app,
    host=settings.server_host,
    port=settings.server_port,
)

