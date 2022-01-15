import hashlib


def md5(s: str):
    m = hashlib.md5()

    if isinstance(s, bytes):
        m.update(s)
    else:
        m.update(bytes(s, "utf8"))

    return m.hexdigest().upper()
