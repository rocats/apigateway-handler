import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .utils import set_body


class PreviewBody(BaseHTTPMiddleware):
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        # Intercept request body
        await set_body(request)
        body = json.dumps(await request.json())
        print(body)

        # Continue processing the request
        response = await call_next(request)

        return response
