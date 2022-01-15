from fastapi import APIRouter
from sqlalchemy import select
from pydantic import BaseModel
from ...db.tables import Account
from ...db.main import session
from ...utils import md5

router = APIRouter(prefix="/account")


class LoginParam(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(param: LoginParam):
    result = session.execute(
        select(Account.username, Account.password).
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


@router.get("/register")
def register():
    return "register"
