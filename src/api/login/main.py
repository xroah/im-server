from fastapi import APIRouter

router = APIRouter(prefix="/login")


@router.get("/")
def login():
    return "login"


@router.get("/register")
def register():
    return "register"
