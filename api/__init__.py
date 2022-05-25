from fastapi import APIRouter
from api.reports import router as report_router
from api.prizes import router as prize_router

router = APIRouter()
router.include_router(report_router)
router.include_router(prize_router)