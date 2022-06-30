from fastapi import APIRouter, Depends, Response, status
from typing import List
from datetime import date

from models.prizes import Prize
from services.prizes import PrizesService

router = APIRouter(
    prefix="/prizes",
    tags=['prizes'])


@router.get("/", response_model=List[Prize])
def get_prizes(service: PrizesService = Depends()):
    """Запрос премий за все месяцы из базы"""
    return service.get_all()


@router.get("/{date}", response_model=Prize)
def get_prize(date: date = None, service: PrizesService = Depends()):
    """Запрос премии за конкретный месяц. Всегда 25 число"""
    return service.get(date)


@router.post("/", response_model=Prize)
def create_prize(prize_data: Prize, service: PrizesService = Depends()):
    """Создание записи в базе премии. Если запись существует, то будет автоматическое обновление. Всегда 25 число"""
    return service.create(prize_data=prize_data)


@router.put('/', response_model=Prize)
def update_prize(date: date, prize_data: Prize, service: PrizesService = Depends()):
    """Обновление записи в базе премии. Всегда 25 число"""
    return service.update(date=date, prize_data=prize_data)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_prize(date: date, service: PrizesService = Depends()):
    """Удаление записи в базе премии. Всегда 25 число"""
    service.delete(date=date)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


