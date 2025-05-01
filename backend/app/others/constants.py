TOKEN_LIFETIME = 15


class Status:
    SUCCESS: str = "OK"
    CREATED: str = "CREATED"
    FAILURE: str = "FAIL"
    UNAUTHORIZED: str = "UNAUTHORIZED"
    ACCESS_DENIED: str = "ACCESS DENIED"
    NOT_FOUND: str = "NOT FOUND"


class Comment:
    SUCCESS: str = "Everything is OK"
    FAILURE: str = "Something went wrong"
    UNAUTHORIZED: str = "User is unauthorized"
    ACCESS_DENIED: str = "Access denied"
    NOT_FOUND: str = "Resource was not found"


class StatusCode:
    SUCCESS: int = 200
    CREATED: int = 201
    FAILURE: int = 400
    UNAUTHORIZED: int = 401
    ACCESS_DENIED: int = 403
    NOT_FOUND: int = 404


class Documentation:
    SWAGGER_URL = "/docs"
    API_URL = "/swagger"
    TAGS = [
        {"name": "Authorization", "description": "Авторизация и регистрация"},
        {"name": "Profile", "description": "Профиль пользователя"},
    ]
