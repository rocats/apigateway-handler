import structlog
from uuid import uuid4
from httpx import AsyncClient
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_binary

router = APIRouter()
logger = structlog.get_logger()


async def forward(url):
    async with AsyncClient() as client:
        return await client.get(url)


@router.post("/webhook")
async def webhook():
    attributes = {
        "id": str(uuid4()),
        "type": "dev.knative.staging.repeater-v3.webhook-relay",
        "source": "dev.knative.staging/repeater-v3/apigateway-interceptor",
    }
    data = {"message": "forwarded payload message to relay service successfully!"}
    event = CloudEvent(attributes, data)
    headers, body = to_binary(event)

    return JSONResponse(
        headers=headers, content=jsonable_encoder(body), status_code=status.HTTP_200_OK
    )
