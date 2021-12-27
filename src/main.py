from fastapi import FastAPI
from api.main import api
import random

app = FastAPI()

app.include_router(api)

@app.get("/")
async def root():
    return "Hello world"

