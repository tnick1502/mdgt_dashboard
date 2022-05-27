from fastapi import APIRouter
from api.reports import router as report_router
from api.prizes import router as prize_router
from api.pay import router as pay_router
from api.authorization import router as authorization_router

router = APIRouter()
router.include_router(report_router)
router.include_router(prize_router)
router.include_router(pay_router)
router.include_router(authorization_router)