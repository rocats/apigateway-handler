import json
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):
    serialized_json = json.dumps(await request.json())
    return JSONResponse(
        content=jsonable_encoder({"payload": json.loads(serialized_json)}),
        status_code=status.HTTP_200_OK,
    )
