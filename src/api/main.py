from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import time
from .routers.account.main import router as account_router

api = FastAPI()
api.include_router(account_router)


@api.get("/")
async def root():
    return "Welcome"


@api.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # if ("authorization" not in request.headers) or (not request.headers["authorization"]):
    #     data = json.dumps({"code": 401, "msg": "没有权限"})
    #
    #     return responses.JSONResponse(status_code=401, content=data)

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={
        "code": -100,
        "msg": "参数错误"
    })
