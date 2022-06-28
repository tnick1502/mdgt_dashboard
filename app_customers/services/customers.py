from typing import List, Optional
from datetime import date
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from models.customers import Customer, CustomerCreate
import db.tables as tables
from db.database import get_session

class CustomerService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, id: int) -> Optional[tables.Customers]:
        staffs = self.session.query(tables.Customers).filter_by(id=id).first()

        if not staffs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return staffs

    def get_all(self) -> List[tables.Customers]:
        return self.session.query(tables.Customers).order_by(tables.Customers.full_name).all()

    def get_month_birthday(self, month) -> List[tables.Customers]:
        return self.session.query(tables.Customers).filter(extract('month', tables.Customers.birthday) == month).order_by(tables.Customers.full_name).all()

    def get_day_birthday(self, month, day) -> List[tables.Customers]:
        return self.session.query(tables.Customers).filter(extract('month', tables.Customers.birthday) == month).filter(extract('day', tables.Customers.birthday) == day).order_by(tables.Customers.full_name).all()

    def get(self, name) -> Optional[tables.Customers]:
        staffs = self.session.query(tables.Customers).all()

        if not staffs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        res = []

        for staff in staffs:
            if name.upper() in str(staff.full_name).upper():
                res.append(staff)
            elif name.upper() in str(staff.organization).upper():
                res.append(staff)

        return res

    def create(self, staff_data: CustomerCreate) -> tables.Customers:
        staff = tables.Customers(
            **staff_data.dict())
        self.session.add(staff)
        self.session.commit()
        return staff

    def update(self, id: int, staff_data: CustomerCreate) -> tables.Customers:
        staff = self._get(id)
        for field, value in staff_data:
            setattr(staff, field, value)
        self.session.commit()
        return staff

    def delete(self, id: str):
        staff = self._get(id)
        self.session.delete(staff)
        self.session.commit()
