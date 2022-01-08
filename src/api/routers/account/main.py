from fastapi import APIRouter
from sqlalchemy import text
from ...db.main import engine

router = APIRouter(prefix="/account")


@router.get("/login")
def login():
    with engine.connect() as conn:
        result = conn.execute(text("select * from account"))
        result = result.all()
    return result


@router.get("/register")
def register():
    return "register"
