from fastapi import FastAPI
from uvicorn import run
from starlette.middleware.base import BaseHTTPMiddleware

from api.v1.middleware.schema_validate import ValidateChannel
from api.v1.middleware.request_body import InterceptRequestBody
from api.v1.middleware.process_time import ProcessTime
from api.v1.router import router

# app
app = FastAPI()

# middlewares
app.add_middleware(BaseHTTPMiddleware, dispatch=ValidateChannel())
app.add_middleware(BaseHTTPMiddleware, dispatch=InterceptRequestBody())
app.add_middleware(BaseHTTPMiddleware, dispatch=ProcessTime())

# router
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    run("index:app", host="0.0.0.0", port=5000, reload=True, workers=1)
