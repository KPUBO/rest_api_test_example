from fastapi import APIRouter

from core.config import settings


from api.api_v1.users import router as user_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(user_router)