import hashlib
from fastapi import Request
from jose import jwt


def md5(s: str):
    m = hashlib.md5()

    if isinstance(s, bytes):
        m.update(s)
    else:
        m.update(s.encode())

    return m.hexdigest().upper()


def encode_token(d: dict):
    return jwt.encode(d, "secret", algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, "secret", algorithms=["HS256"])


def get_token_from_header(req: Request):
    name = "Authentication"
    headers = req.headers
    prefix = "Bearer "

    if name not in headers:
        return None

    token = headers[name] or ""

    if not token.startswith(prefix):
        return None

    return token.removeprefix(prefix)


def decode_token_from_header(req: Request):
    token = get_token_from_header(req)

    if token is None:
        return None

    return decode_token(token)


def get_key(userid: str, username: str):
    return f"{userid}_{username}"
