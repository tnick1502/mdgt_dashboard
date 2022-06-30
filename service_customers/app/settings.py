from pydantic import BaseSettings


customers = "/databases/customers/"
#customers = "/home/nick/databases/customers/"

class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 9600

    photo_path: str = f'{customers}photos'
    excel_file: str = f'{customers}customers.xlsx'
    database_url: str = f'sqlite:///{customers}customers.sqlite3'

settings = Settings()
