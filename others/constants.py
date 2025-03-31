class Status:
    SUCCESS: str = "OK"
    FAILURE: str = "FAIL"
    ACCESS_DENIED: str = "ACCESS DENIED"
    NOT_FOUND: str = "NOT FOUND"


class Comment:
    SUCCESS: str = "Everything is OK"
    FAILURE: str = "Something went wrong"


class StatusCode:
    SUCCESS: int = 200
    FAILURE: int = 400
    ACCESS_DENIED: int = 403
    NOT_FOUND: int = 404
