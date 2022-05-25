import uvicorn
from settings import settings
from app import app

uvicorn.run(
    app,
    host=settings.server_host,
    port=settings.server_port,
)

