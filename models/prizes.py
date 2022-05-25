from pydantic import BaseModel
from datetime import date

class Prize(BaseModel):
    date: date
    prize: float

    class Config:
        orm_mode = True