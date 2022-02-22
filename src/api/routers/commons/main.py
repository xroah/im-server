from fastapi import APIRouter
import uuid

from .verificationcode import img2base64, gen_code
from ...db.redis import veri_code_db

router = APIRouter(prefix="/commons")


@router.get("/get_code")
async def get_code():
    code_key = str(uuid.uuid4())
    code = gen_code()
    veri_code_db.set(code_key, code["code"], 5 * 60)

    return {
        "code_key": uuid.uuid4(),
        "code_img": img2base64(code["image"])
    }
