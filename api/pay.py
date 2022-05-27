from fastapi import APIRouter, Depends, Response, status
import datetime
from datetime import date
from typing import Optional
from models.authorization import User
from services.authorization import AuthService, get_current_user

from services.pay import PayService

router = APIRouter(
    prefix="/pay",
    tags=['pay'])


@router.get("/", response_model=list)
def get_pays(service: PayService = Depends(), user: User = Depends(get_current_user)):
    return service.get_pay()


@router.get("/{date}", response_model=dict)
def get_pay(date: Optional[date], service: PayService = Depends(), user: User = Depends(get_current_user)):
    return service.get_one_pay(date)
