from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "Ok", "message": "pong"}

@router.get("/healthz")
async def healthz():
    return {"status":"healthy"}
