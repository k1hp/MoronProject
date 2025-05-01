from flask import Flask, jsonify
from flask_restx import Api

from database.creation import db
from app.others.settings import DB_CONNECTION, DB_NAME
from app.apis.authorization import (
    api as ns_authorization,
)
from app.apis.profile import api as ns_profile
from database.flask_managers import DatabaseAdder
from app.others.helpers import AccessToken, Password
from app.documentation.swagg import swagger_ui_blueprint, get_apispec
from app.others.constants import Documentation


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION + DB_NAME
db.init_app(app)

api = Api(app, title="Morons API")
api.add_namespace(ns_authorization, path="/api")
api.add_namespace(ns_profile, path="/api")

app.register_blueprint(swagger_ui_blueprint, url_prefix=Documentation.SWAGGER_URL)


@app.route("/swagger")
def create_swagger_spec():
    return jsonify(get_apispec(app).to_dict())


with app.app_context():
    db.drop_all()
    db.create_all()


with app.app_context():
    adder = DatabaseAdder()
    access_token = AccessToken().hash
    adder.add_user("chelik", "4@yandex.ru", Password("1234").hash)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # нужно слушать по всем, иначе нельзя подключиться
