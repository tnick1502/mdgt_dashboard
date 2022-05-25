from fastapi import APIRouter, Depends, Response, status
from typing import List, Optional

from models.reports import Report
#from models.auth import User
from database import Session, get_session
from services.reports import ReportsService
#from services.auth import get_current_user
from models.reports import Report
import tables

router = APIRouter(
    prefix="/reports",
    tags=['operations'],
)

@router.get("/", response_model=List[Report])
def get_reports(service: ReportsService = Depends()):
    return service.get_all()

@router.post("/", response_model=Report)
def create_operations(
        operation_data: OperationCreate,
        user: User = Depends(get_current_user),
        service: OperationService = Depends()):
    return service.create(user_id=user.id, operation_data=operation_data)

@router.get('/{operation_id}', response_model=Operation)
def get_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    service: OperationService = Depends()):
    return service.get(user_id=user.id, operation_id=operation_id)


@router.put('/{operation_id}', response_model=Operation)
def update_operation(
    operation_id: int,
    operation_data: OperationUpdate,
    user: User = Depends(get_current_user),
    service: OperationService = Depends(),
):
    return service.update(
        user_id=user.id,
        operation_id=operation_id,
        operation_data=operation_data,
    )


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT,
)
def delete_operation(
    operation_id: int,
    user: User = Depends(get_current_user),
    operations_service: OperationService = Depends(),
):
    operations_service.delete(
        user_id=user.id,
        operation_id=operation_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


