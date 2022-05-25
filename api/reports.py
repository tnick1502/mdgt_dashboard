from fastapi import APIRouter, Depends, Response, status
from typing import List
from datetime import date

from models.reports import Report, ReportCreate
from services.reports import ReportsService

router = APIRouter(
    prefix="/reports",
    tags=['reports'])


@router.get("/", response_model=List[Report])
def get_reports(date: date = None, service: ReportsService = Depends()):
    if date:
        return service.get(date)
    return service.get_all()


@router.post("/", response_model=Report)
def create_reports(report_data: ReportCreate, service: ReportsService = Depends()):
    return service.create(report_data=report_data)


@router.put('/{date}', response_model=Report)
def update_report(date: date, report_data: Report, service: ReportsService = Depends()):
    return service.update(date=date, report_data=report_data)


@router.delete('/{date}', status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(date: date, service: ReportsService = Depends()):
    service.delete(date=date)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


