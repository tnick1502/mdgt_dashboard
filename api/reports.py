from fastapi import APIRouter, Depends, Response, status
from typing import List
from datetime import date

from models.reports import Report, ReportCreate
from services.reports import ReportsService

router = APIRouter(
    prefix="/reports",
    tags=['reports'])


@router.get("/", response_model=List[Report])
def get_reports(service: ReportsService = Depends()):
    """Запрос отчетов за все месяцы из базы"""
    return service.get_all()

@router.get("/{date}", response_model=Report)
def get_report(date: date = None, service: ReportsService = Depends()):
    """Запрос отчета за конкретный месяц. Всегда 25 число"""
    return service.get(date)


@router.post("/", response_model=Report)
def create_reports(report_data: ReportCreate, service: ReportsService = Depends()):
    """Создание записи в базе отчетов. Если запись существует, то будет автоматическое обновление. Всегда 25 число"""
    return service.create(report_data=report_data)


@router.put('/{date}', response_model=Report)
def update_report(date: date, report_data: Report, service: ReportsService = Depends()):
    """Обновление записи в базе премии. Всегда 25 число"""
    return service.update(date=date, report_data=report_data)


@router.delete('/{date}', status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(date: date, service: ReportsService = Depends()):
    """Удаление записи в базе премии. Всегда 25 число"""
    service.delete(date=date)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


