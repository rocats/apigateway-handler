from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/health")
async def health():
    return JSONResponse(
        content=jsonable_encoder({"health": "ok!"}), status_code=status.HTTP_200_OK
    )
