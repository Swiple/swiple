from fastapi import APIRouter
from starlette.responses import JSONResponse


router = APIRouter()


@router.get("/health", name="Health check")
def health():
    return JSONResponse(status_code=200)
