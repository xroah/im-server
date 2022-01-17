from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from jose import jwt
from ...db.tables import Account
from ...db.main import Session
from ...utils import md5

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

    return {
        "code": 0,
        "msg": "登录成功!"
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
            userid = new_user.userid
            s.commit()
    except IntegrityError as e:
        return {
            "code": -2,
            "msg": "该用户名已被使用"
        }
    except Exception as e:
        return {
            "code": -1,
            "msg": e
        }

    return {
        "code": 0,
        "msg": "注册成功",
        "data": userid
    }


