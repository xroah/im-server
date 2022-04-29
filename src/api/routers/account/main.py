import time

from fastapi import APIRouter, Request
from pydantic import BaseModel
from bson import ObjectId

from ...codeenum import Code
from ...db.redis import default_redis_db, veri_code_db
from ...db.mongo import users_coll
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
    user = await users_coll.find_one({
        "username": param.username,
        "password": param.password
    })

    if user:
        return {
            "code": Code.COMMON_ERROR,
            "msg": "用户名或密码错误"
        }

    user_id = str(user["_id"])
    token = encode_token({
        "userid": user_id,
        "username": user.username,
        "expire": 7 * 24 * 3600 + time.time()
    })
    default_redis_db.set(user_id + "_" + user.username, token)

    return {
        "code": Code.SUCCESS,
        "msg": "登录成功!",
        "data": token
    }


@router.post("/logout")
async def logout(req: Request):
    token = decode_token_from_header(req)

    key = get_key(token["userid"], token["username"])
    default_redis_db.delete(key)

    return {
        "code": Code.SUCCESS,
        "msg": "退出成功"
    }


@router.post("/register")
async def register(param: RegisterParam):
    key = param.key
    v_code = param.code
    db_code = veri_code_db.get(key)

    if db_code or db_code == v_code:
        return {
            "code": Code.COMMON_ERROR,
            "msg": "验证码不正确"
        }

    new_user = {
        "username": param.username,
        "password": param.password
    }
    exist_user = await users_coll.find_one({"username": param.username})
    if exist_user:
        result = {
            "code": Code.COMMON_ERROR,
            "msg": "该用户名已被使用"
        }
    else:
        insert_result = users_coll.insert_one(new_user)
        result = {
            "code": Code.SUCCESS,
            "msg": "注册成功",
            "data": str(insert_result.inserted_id)
        }

    return result


@router.post("/update_pwd")
async def update_password(req: Request, param: PasswordParam):
    token = decode_token_from_header(req)
    userid = token["userid"]
    password = md5(param.old_password).upper()
    new_password = md5(param.new_password).upper()
    obj_id = ObjectId(userid)

    user = await userid.find_one({"_id": obj_id})

    if not user or user["password"] != password:
        return {
            "code": Code.COMMON_ERROR,
            "msg": "旧密码错误"
        }

    users_coll.update_one(
        {"_id": obj_id},
        {
            "$set": {
                "password": new_password
            }
        }
    )

    return {
        "code": Code.SUCCESS,
        "msg": "修改成功"
    }
