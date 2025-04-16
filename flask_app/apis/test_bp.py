from flask_restx import Resource, Namespace

api = Namespace('burgers', description='Yu can eat burger')

@api.route("/hello")
class Burger(Resource):
    def get(self):
        return {"hello": "world"}