from fastapi import APIRouter, Depends, Response, status
from typing import List
from datetime import date

from models.staff import Staff, StaffCreate, StaffCreate
from services.staff import StaffService

router = APIRouter(
    prefix="/staff",
    tags=['staff'])


@router.get("/", response_model=List[Staff])
def get_staffs(service: StaffService = Depends()):
    """Запрос всех сотрудников"""
    return service.get_all()


@router.get("/{name}", response_model=List[Staff])
def get_staff(name: str, service: StaffService = Depends()):
    """Запрос осотрудника по имени"""
    return service.get(name)


@router.post("/", response_model=Staff)
def create_staff(staff_data: StaffCreate, service: StaffService = Depends()):
    """Создание сотрудника"""
    return service.create(staff_data=staff_data)


@router.put('/{id}', response_model=Staff)
def update_staff(id: int, staff_data: StaffCreate, service: StaffService = Depends()):
    """Обновление данных сотрудника"""
    return service.update(id=id, staff_data=staff_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(id: int, service: StaffService = Depends()):
    """Удаление сотрудника"""
    service.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/month_birthday/", response_model=List[Staff])
def get_month_birthday(month: int, service: StaffService = Depends()):
    """Запрос дней рождений за месяц"""
    return service.get_month_birthday(month=month)


@router.get("/day_birthday/", response_model=List[Staff])
def get_day_birthday(month: int, day: int, service: StaffService = Depends()):
    """Запрос дней рождений за месяц"""
    return service.get_day_birthday(month=month, day=day)
