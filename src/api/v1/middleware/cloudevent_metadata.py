import json
import structlog
from typing import Any
from fastapi import Request
from cloudevents.http import from_http, CloudEvent

from constant import BASE_API_PATH


class CloudEventMetadata:
    def __init__(self):
        pass

    def new_event(self, data: Any) -> CloudEvent:
        attributes = {
            "type": "apigateway.interceptor",
            "producer": "apigateway.interceptor",
            "source": "telegram_server",
            "protocol": "http",
        }
        return CloudEvent(attributes, data)

    async def __call__(self, request: Request, call_next):
        logger = structlog.get_logger()

        # extract event
        if str(request.url).split(BASE_API_PATH)[1] != "/health":
            body = json.dumps(await request.json())
            event = from_http(dict(request.headers), body)

            # construct logger
            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(
                path=request.url.path,
                method=request.method,
                client_host=request.client.host,  # type:ignore
                request_id=event["id"],
                event_source=event["source"],
                event_type=event["type"],
            )

            logger.info("Received a cloudevent")
            logger.info(f"Body: {event.get_data()}")

        response = await call_next(request)

        return response
