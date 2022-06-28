import uvicorn
from settings import settings
from app import app
from background_tasks import parser
from threading import Thread

if __name__ == "__main__":

    parser_thread = Thread(
        target=parser,
        args=(86400,),
        daemon=True,
    ).start()

    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
    )



