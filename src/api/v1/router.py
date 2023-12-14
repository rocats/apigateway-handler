from fastapi import APIRouter

from .endpoint import health
from .endpoint import webhook

router = APIRouter()

router.include_router(health.router, tags=["Health"])
router.include_router(webhook.router, tags=["Health"])
