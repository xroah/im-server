from fastapi import APIRouter
from .login import main

api = APIRouter(prefix="/api")
api.include_router(main.router)


@api.get("/")
async def root():
    return "Welcome"
