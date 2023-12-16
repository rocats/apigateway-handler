from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class InterceptRequestBody(BaseHTTPMiddleware):
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        # Intercept request body
        await self.set_body(request)

        # Continue processing the request
        response = await call_next(request)

        return response

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive
