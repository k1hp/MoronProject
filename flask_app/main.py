from flask import Flask, request
from flask_restx import Api, Resource
from flasgger import Swagger, APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

from database.creation import db, check_exists_db
from others.settings import DB_CONNECTION, DB_NAME
from flask_app.apis.authorization import (
    api as ns1,
)
from flask_app.apis.profile import api as ns2
from database.managers import DatabaseAdder, DatabaseSelector
from others.helpers import AccessToken, RefreshToken, Password
from others.responses import CommentResponse
from flask_app.models.input_models import UserSchema

# import testik
# from utils import custom_driver

check_exists_db()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION + DB_NAME
db.init_app(app)

api = Api(app)
# app.config["SWAGGER"] = {"openapi": "3.0.2"}
api.add_namespace(ns1, path="/api")
api.add_namespace(ns2, path="/api")
# api.add_resource(Registration, "/api/token/registration")
# api.add_resource(LoginToken, "/api/token/auth/")
# api.add_resource(LoginTempToken, "/api/token/auth/temporary")
# api.add_resource(TokenRefresher, "/api/token/refresh")
# api.add_resource(Logout, "/api/token/logout")

spec = APISpec(
    title="genii",
    version="1.0.0",
    openapi_version="2.0",  # нужна третья версия
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

template = spec.to_flasgger(
    app,
    definitions=[
        UserSchema,
    ],
)

swagger = Swagger(app, template=template)

with app.app_context():
    db.drop_all()

with app.app_context():
    db.create_all()

with app.app_context():
    adder = DatabaseAdder()
    access_token = AccessToken().hash
    adder.add_user("chelik", "4@yandex.ru", Password("1234").hash)
    # driver = custom_driver.our_driver()
    # adder.add_processors(data=testik.parse_processors(driver=driver))
    # adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # try:
    #     adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # except ValueError as e:
    #     print(e)

with app.app_context():
    print(CommentResponse().success_response())


if __name__ == "__main__":
    app.run(debug=True)
