from fastapi import APIRouter

from .endpoints import health
from .endpoints import webhook

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(webhook.router, tags=["Health"])
