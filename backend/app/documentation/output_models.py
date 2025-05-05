import marshmallow as ma
from backend.app.others.constants import Status, Comment


class CreatedResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.CREATED)
    comment = ma.fields.Str(required=True, example="Пользователь успешно создан")


class SuccessResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.SUCCESS)
    comment = ma.fields.Str(required=True, example=Comment.SUCCESS)


class FailureResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.FAILURE)
    comment = ma.fields.Str(required=True, example=Comment.FAILURE)


class UnauthorizedResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.UNAUTHORIZED)
    comment = ma.fields.Str(required=True, example=Comment.UNAUTHORIZED)


class AccessDeniedResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.ACCESS_DENIED)
    comment = ma.fields.Str(required=True, example=Comment.ACCESS_DENIED)


class FailureRegistrationResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.FAILURE)
    comment = ma.fields.Str(
        required=True, example="Пользователь с таким Email уже существует"
    )


class FailureAuthorizationResponseSchema(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.FAILURE)
    comment = ma.fields.Str(required=True, example="Неверный пароль")


class ExistsTokenAuthorizationFailure(ma.Schema):
    status = ma.fields.Str(required=True, example=Status.ACCESS_DENIED)
    comment = ma.fields.Str(required=True, example="Токен уже есть в куках.")
