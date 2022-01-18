from enum import IntEnum


# enum for response code
class Code(IntEnum):
    SUCCESS = 0
    NO_PERM = 401  # no permission
    UNKNOWN_ERROR = 1000  # unknown error
    FILED_ERROR = 1001  # wrong fields of request body
    REG_ERROR = 1002  # register error, such as the username already exists
    LOGIN_ERROR = 1003  # login error, such as wrong password

