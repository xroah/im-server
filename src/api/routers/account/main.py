from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from jose import jwt
from ...db.tables import Account
from ...db.main import Session
from ...utils import md5
from ...db.redis import Redis
from ...utils import encode_token, decode_token
import time


router = APIRouter(prefix="/account")


class LoginParam(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(param: LoginParam):
    result = Session().execute(
        select(Account.userid, Account.username, Account.password).
        where(
            Account.username == param.username,
            Account.password == md5(param.password)
        ).
        limit(1)
    ).all()

    if len(result) == 0:
        return {"code": -1, "msg": "用户名或密码错误"}

    result = result[0]

    token = encode_token({
        "userid": result.userid,
        "username": result.username,
        "expire": 7 * 24 * 3600 + time.time()
    })
    Redis.set(str(result.userid) + "_" + result.username, token)

    return {
        "code": 0,
        "msg": "登录成功!",
        "data": token
    }


@router.post("/register")
async def register(param: LoginParam):
    new_user = Account(
        username=param.username,
        password=md5(param.password)
    )

    try:
        with Session() as s:
            s.add(new_user)
            s.flush()
            userid = new_user.userid
            s.commit()
    except IntegrityError:
        result = {
            "code": -2,
            "msg": "该用户名已被使用"
        }
    except Exception as e:
        result = {
            "code": -1,
            "msg": e
        }
    else:
        result = {
            "code": 0,
            "msg": "注册成功",
            "data": userid
        }

    return result
