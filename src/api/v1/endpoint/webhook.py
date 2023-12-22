import structlog
from uuid import uuid4
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary

from config import WebhookConfig

router = APIRouter()
logger = structlog.get_logger()


@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    attributes = {
        "id": str(uuid4()),
        "type": WebhookConfig.CE_TYPE,
        "source": WebhookConfig.CE_SOURCE,
    }
    logger.debug("Forwarded payload message to relay service successfully!")
    event = CloudEvent(attributes, payload)
    headers, body = to_binary(event)

    return JSONResponse(
        headers=headers, content=jsonable_encoder(body), status_code=status.HTTP_200_OK
    )
