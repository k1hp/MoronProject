from flask import Flask, jsonify, render_template
from flask_restx import Api

from backend.database.creation import db
from backend.app.others.settings import DB_CONNECTION, DB_NAME
from backend.app.apis.authorization import (
    api as ns_authorization,
)
from backend.app.apis.components import api as ns_components
from backend.app.apis.profile import api as ns_profile
from backend.database.flask_managers import DatabaseAdder, add_components, get_component
from backend.app.services.helpers import AccessToken, Password
from backend.app.documentation.swagg import swagger_ui_blueprint, get_apispec
from backend.app.others.constants import Documentation


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION + DB_NAME
db.init_app(app)

api = Api(app, title="Morons API", doc=False)
# swagger = Swagger(app)
#
api.add_namespace(ns_authorization, path="/api")
api.add_namespace(ns_profile, path="/api")
api.add_namespace(ns_components, path="/api/components")
# api.add_resource(Registration, "/api/registration")

app.register_blueprint(swagger_ui_blueprint, url_prefix=Documentation.SWAGGER_URL)


@app.errorhandler(404)
def not_found(error):
    return (render_template("redirect_on_doc.html", title="Not Found"), 404)


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
    add_components()
    print(get_component("processors"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # нужно слушать по всем, иначе нельзя подключиться
