from typing import List
from os import getenv
from dotenv import load_dotenv
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


load_dotenv()


class ValidateChannel:
    def __init__(self):
        self.whitelist_channels = self.get_whitelist_channels()

    async def __call__(self, request: Request, call_next):
        if request.method == "POST" and str(request.url).split("/api/v1")[1] in [
            "/webhook"
        ]:
            body = await request.json()
            if str(body["message"]["chat"]["id"]) in self.get_whitelist_channels():
                response = await call_next(request)
                return response
            else:
                return JSONResponse(
                    content=jsonable_encoder(
                        {"message": "channel is not within whitelist, aborted"}
                    ),
                    status_code=status.HTTP_417_EXPECTATION_FAILED,
                )
        else:
            response = await call_next(request)
            return response

    def get_whitelist_channels(self) -> List[str]:
        return getenv("WHITELIST_CHANNELS", "").split(",")
