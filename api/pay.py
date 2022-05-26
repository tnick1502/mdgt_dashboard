from fastapi import APIRouter, Depends, Response, status
import datetime
from datetime import date
from typing import Optional

from services.pay import PayService

router = APIRouter(
    prefix="/pay",
    tags=['pay'])


@router.get("/")
def get_prizes(date: Optional[date] = None, service: PayService = Depends()):
    return service.get_pay(date)
