from fastapi import Request, FastAPI, responses
import time
import json
from .login import main

api = FastAPI()
api.include_router(main.router)


@api.get("/")
async def root():
    return "Welcome"


@api.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    if ("authorization" not in request.headers) or (not request.headers["authorization"]):
        data = json.dumps({"code": 401, "msg": "没有权限"})

        return responses.JSONResponse(status_code=401, content=data)

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response
