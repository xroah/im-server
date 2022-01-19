import time

from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from ...codeenum import Code
from ...db.main import Session
from ...db.redis import Redis
from ...db.tables import Account
from ...utils import (
    encode_token,
    decode_token_from_header,
    get_key
)
from ...utils import md5

router = APIRouter(prefix="/account")


class LoginParam(BaseModel):
    username: str
    password: str


class RegisterParam(LoginParam):
    key: str
    code: str


class PasswordParam(BaseModel):
    new_password: str
    old_password: str


@router.post("/login")
async def login(param: LoginParam):
    with Session() as s:
        result = s.execute(
            select(
                Account.userid,
                Account.username,
                Account.password
            ).where(
                Account.username == param.username,
                Account.password == md5(param.password)
            ).limit(1)
        ).all()

    if len(result) == 0:
        return {
            "code": Code.COMMON_ERROR,
            "msg": "用户名或密码错误"
        }

    result = result[0]

    token = encode_token({
        "userid": result.userid,
        "username": result.username,
        "expire": 7 * 24 * 3600 + time.time()
    })
    Redis.set(str(result.userid) + "_" + result.username, token)

    return {
        "code": Code.SUCCESS,
        "msg": "登录成功!",
        "data": token
    }


@router.post("/logout")
async def logout(req: Request):
    token = decode_token_from_header(req)

    key = get_key(token["userid"], token["username"])
    Redis.delete(key)

    return {
        "code": Code.SUCCESS,
        "msg": "退出成功"
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
            "code": Code.COMMON_ERROR,
            "msg": "该用户名已被使用"
        }
    except Exception as e:
        result = {
            "code": Code.UNKNOWN_ERROR,
            "msg": e
        }
    else:
        result = {
            "code": Code.SUCCESS,
            "msg": "注册成功",
            "data": userid
        }

    return result


@router.post("/update_pwd")
async def update_password(req: Request, param: PasswordParam):
    token = decode_token_from_header(req)
    userid = token["userid"]
    password = md5(param.old_password).upper()
    new_password = md5(param.new_password).upper()

    with Session() as s:
        result = s.execute(
            select(Account.userid).where(
                Account.userid == userid,
                Account.password == password
            )
        ).all()

    if len(result) == 0:
        return {
            "code": Code.COMMON_ERROR,
            "msg": "旧密码错误"
        }

    with Session() as s:
        s.execute(
            update(Account).
                where(Account.userid == userid).
                values(password=new_password)
        )
        s.commit()

    return {
        "code": Code.SUCCESS,
        "msg": "修改成功"
    }
