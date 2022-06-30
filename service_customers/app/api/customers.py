import os.path

from fastapi import APIRouter, Response, HTTPException, status, Depends
from typing import List
from fastapi.responses import FileResponse

from models.customers import CustomerCreate, Customer
from services.customers import CustomerService
from settings import settings


router = APIRouter(
    prefix="/customers",
    tags=['customers'])


@router.get("/", response_model=List[Customer])
def get_customers(service: CustomerService = Depends()):
    """Запрос всех заказчиков"""
    return service.get_all()


@router.get("/{name}", response_model=List[Customer])
def get_customer(name: str, service: CustomerService = Depends()):
    """Запрос заказчика по имени"""
    return service.get(name)


@router.post("/", response_model=Customer)
def create_customer(staff_data: CustomerCreate, service: CustomerService = Depends()):
    """Создание заказчика"""
    return service.create(staff_data=staff_data)


@router.put('/', response_model=Customer)
def update_customer(id: int, staff_data: CustomerCreate, service: CustomerService = Depends()):
    """Обновление данных заказчика"""
    return service.update(id=id, staff_data=staff_data)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, service: CustomerService = Depends()):
    """Удаление заказчика"""
    service.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/month_birthday/", response_model=List[Customer])
def get_month_birthday(month: int, service: CustomerService = Depends()):
    """Запрос дней рождений за месяц"""
    return service.get_month_birthday(month=month)


@router.get("/day_birthday/", response_model=List[Customer])
def get_day_birthday(month: int, day: int, service: CustomerService = Depends()):
    """Запрос дней рождений за день"""
    return service.get_day_birthday(month=month, day=day)


@router.get("/get_photo/{id}")
def get_customer_photo(id: int):
    """Запрос фото заказчика"""
    files_dir = os.path.join(settings.photo_path, str(id))
    if not os.path.exists(files_dir):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    files = os.listdir(files_dir)

    for i, file in enumerate(files):
        if ".jpg" not in file:
            files.pop(i)

    if len(files):
        return FileResponse(path=os.path.join(files_dir, files[0]), media_type="image/jpg")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

