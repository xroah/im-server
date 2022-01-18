from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import time
from .routers.account.main import router as account_router
from .utils import get_token_from_header, decode_token
from .db.redis import Redis
from .codeenum import Code

api = FastAPI()
api.include_router(account_router)


@api.get("/")
async def root():
    return "Welcome"


@api.middleware("http")
async def interceptor(request: Request, call_next):
    start_time = time.time()
    path_whitelist = {"/api/account/login", "/api/account/register"}

    if request.url.path not in path_whitelist:
        token = get_token_from_header(request)
        msg = ""

        if token is None:
            msg = "没有权限"
        else:
            try:
                decoded_token = decode_token(token)
            except:
                msg = "token解析错误"
            else:
                if ("userid" not in decoded_token or
                        "username" not in decoded_token or
                        "expire" not in decoded_token):
                    msg = "token格式错误"
                else:
                    userid = decoded_token["userid"]
                    username = decoded_token["username"]
                    expire = decoded_token["expire"]
                    saved_token = Redis.get(f"{userid}_{username}")

                    if expire < time.time() or saved_token != token:
                        msg = "登录已过期, 请重新登录"

        if msg:
            return JSONResponse(
                status_code=401,
                content={
                    "code": Code.NO_PERM,
                    "msg": msg
                }
            )

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={
        "code": Code.FILED_ERROR,
        "msg": "参数错误"
    })
