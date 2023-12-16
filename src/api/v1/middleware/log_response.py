import structlog
from fastapi import Request, Response

from constant import BASE_API_PATH


class LogResponse:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        logger = structlog.get_logger()
        response: Response = await call_next(request)

        structlog.contextvars.bind_contextvars(
            status_code=response.status_code,
        )

        # Exclude /healthcheck endpoint from producing logs
        if request.url.path != BASE_API_PATH + "/health":
            if 400 <= response.status_code < 500:
                logger.warn("Client error or unexpected event, aborted")
            elif response.status_code >= 500:
                logger.error("Internal server error")
            else:
                logger.info("OK")
        else:
            logger.info("Healthcheck OK")

        return response
