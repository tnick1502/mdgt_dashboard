from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.normpath(".env"))

class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 9000

    photo_path: str = f'{os.getenv("CUSTOMERS")}photos'
    excel_file: str = f'{os.getenv("CUSTOMERS")}customers.xlsx'
    database_url: str = f'sqlite:///{os.getenv("CUSTOMERS")}customers.sqlite3'

settings = Settings()
