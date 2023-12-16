import structlog
from fastapi import FastAPI
from uvicorn import run
from starlette.middleware.base import BaseHTTPMiddleware

from constant import LOCAL_DEV_PORT
from api.v1.middleware.cloudevent_metadata import CloudEventMetadata
from api.v1.middleware.schema_validate import ValidateChannel
from api.v1.middleware.request_body import InterceptRequestBody
from api.v1.middleware.process_time import ProcessTime
from api.v1.router import router

# app
app = FastAPI()

# router
app.include_router(router, prefix="/api/v1")

# middlewares
app.add_middleware(BaseHTTPMiddleware, dispatch=CloudEventMetadata())
app.add_middleware(BaseHTTPMiddleware, dispatch=ValidateChannel())
app.add_middleware(BaseHTTPMiddleware, dispatch=InterceptRequestBody())
app.add_middleware(BaseHTTPMiddleware, dispatch=ProcessTime())

if __name__ == "__main__":
    logger = structlog.get_logger()
    logger.info(f"App loaded, listen on port {LOCAL_DEV_PORT}")
    run(
        "index:app",
        host="0.0.0.0",
        port=LOCAL_DEV_PORT,
        reload=True,
        workers=1,
        log_config=None,
    )
