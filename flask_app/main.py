from flask import Flask, request
from flask_restx import Api, Resource
from flasgger import Swagger

from database.creation import db
from others.settings import DB_CONNECTION
from flask_app.apis.authorization import (
    api as ns1,
)
from flask_app.apis.profile import api as ns2
from database.managers import DatabaseAdder, DatabaseSelector
from others.helpers import AccessToken, RefreshToken, Password
from others.responses import CommentResponse

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION
db.init_app(app)

api = Api(app)
swagger = Swagger(app)
api.add_namespace(ns1, path="/api")
api.add_namespace(ns2, path="/api")
# api.add_resource(Registration, "/api/token/registration")
# api.add_resource(LoginToken, "/api/token/auth/")
# api.add_resource(LoginTempToken, "/api/token/auth/temporary")
# api.add_resource(TokenRefresher, "/api/token/refresh")
# api.add_resource(Logout, "/api/token/logout")

with app.app_context():
    db.drop_all()

with app.app_context():
    db.create_all()

with app.app_context():
    adder = DatabaseAdder()
    access_token = AccessToken().hash
    adder.add_user("nigger", "4@yandex.ru", Password("1234").hash)
    # adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # try:
    #     adder.add_tokens(1, "d", access_token, RefreshToken().hash, revoked=True)
    # except ValueError as e:
    #     print(e)

with app.app_context():
    print(CommentResponse().success_response())


if __name__ == "__main__":
    app.run(debug=True)
