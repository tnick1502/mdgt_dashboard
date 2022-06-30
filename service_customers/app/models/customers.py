from pydantic import BaseModel
from datetime import date


class CustomerBase(BaseModel):
    full_name: str
    phone_number: int
    email: str
    sex: str
    birthday: date
    organization: str
    level: str


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class CustomerCreate(CustomerBase):
    pass
