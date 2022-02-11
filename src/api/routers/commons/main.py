from fastapi import APIRouter
import uuid

from .verificationcode import img2base64, gen_code
from ...db.redis import Redis

router = APIRouter(prefix="/commons")
redis_db = Redis(1)


@router.get("/get_code")
async def get_code():
    code_key = str(uuid.uuid4())
    code = gen_code()
    redis_db.set(code_key, code["code"], 5 * 60)

    return {
        "code_key": uuid.uuid4(),
        "code_img": img2base64(code["image"])
    }
