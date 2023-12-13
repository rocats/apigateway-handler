from uuid import uuid4
from fastapi import Request


class RequestId:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-API-Request-Id"] = str(uuid4())
        return response
