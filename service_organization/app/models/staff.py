from pydantic import BaseModel
from datetime import date

class StaffBase(BaseModel):
    full_name: str
    phone: int
    birthday: date

class Staff(StaffBase):
    id: int
    class Config:
        orm_mode = True

class StaffCreate(StaffBase):
    pass
