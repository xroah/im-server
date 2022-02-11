from fastapi import APIRouter
import uuid
from .verificationcode import img2base64, gen_code_img

router = APIRouter(prefix="/commons")


@router.get("/get_code")
async def get_code():
    return {
        "code_key": uuid.uuid4(),
        "code_img": img2base64(gen_code_img())
    }
