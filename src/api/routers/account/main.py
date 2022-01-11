from fastapi import APIRouter
from sqlalchemy import text, select
from ...db.tables import Account, engine, session

router = APIRouter(prefix="/account")


@router.get("/login")
def login():
    result = session.execute(select(Account.username, Account.password).limit(1).offset(1))

    return result.all()


@router.get("/register")
def register():
    return "register"
