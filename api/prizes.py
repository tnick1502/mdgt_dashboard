from fastapi import APIRouter, Depends, Response, status
from typing import List
from datetime import date

from models.prizes import Prize
from services.prizes import PrizesService

router = APIRouter(
    prefix="/prizes",
    tags=['prizes'])


@router.get("/", response_model=List[Prize])
def get_prizes(date: date = None, service: PrizesService = Depends()):
    if date:
        return service.get(date)
    return service.get_all()


@router.post("/", response_model=Prize)
def create_prize(prize_data: Prize, service: PrizesService = Depends()):
    return service.create(prize_data=prize_data)


@router.put('/{date}', response_model=Prize)
def update_prize(date: date, prize_data: Prize, service: PrizesService = Depends()):
    return service.update(date=date, prize_data=prize_data)


@router.delete('/{date}', status_code=status.HTTP_204_NO_CONTENT)
def delete_prize(date: date, service: PrizesService = Depends()):
    service.delete(date=date)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


