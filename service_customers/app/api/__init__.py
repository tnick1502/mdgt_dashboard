from fastapi import APIRouter
from api.customers import router as customers_router

router = APIRouter()
router.include_router(customers_router)