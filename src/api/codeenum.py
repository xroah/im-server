from enum import IntEnum


# enum for response code
class Code(IntEnum):
    SUCCESS = 0
    NO_PERM = 401  # no permission
    UNKNOWN_ERROR = 1000  # unknown error
    COMMON_ERROR = 1001
