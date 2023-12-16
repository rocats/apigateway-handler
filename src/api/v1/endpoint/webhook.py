import os
from httpx import AsyncClient, HTTPError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


async def forward(url):
    async with AsyncClient() as client:
        return await client.get(url)


@router.post("/webhook")
async def webhook():
    try:
        res = await forward(os.getenv("RELAY_SERVICE_ENDPOINT", ""))

        if res.status_code == status.HTTP_200_OK:
            return JSONResponse(
                content=jsonable_encoder(
                    {
                        "message": "forwarded payload message to relay service successfully!"
                    }
                ),
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPError("Failed to relay message to designated service")
    except HTTPError as err:
        return JSONResponse(
            content=jsonable_encoder({"error": str(err)}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
