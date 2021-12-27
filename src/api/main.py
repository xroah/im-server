from fastapi import APIRouter

api = APIRouter(prefix="/api")

@api.get("/")
async def root():
    return "API"