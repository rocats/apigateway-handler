from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter()


@router.post("/health")
async def health():
    return Response(content="", status_code=status.HTTP_204_NO_CONTENT)
