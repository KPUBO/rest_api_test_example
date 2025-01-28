from fastapi import APIRouter

from core.config import settings

from api.api_v1.routers.activities import router as activity_router
from api.api_v1.routers.phones import router as phones_router
from api.api_v1.routers.buildings import router as buildings_router
from api.api_v1.routers.organizations import router as organizations_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)

router.include_router(activity_router)
router.include_router(phones_router)
router.include_router(buildings_router)
router.include_router(organizations_router)
