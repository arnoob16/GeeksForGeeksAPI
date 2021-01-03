from flask import Flask, redirect
from flask_restful import Api, Resource
import scrap

app = Flask(__name__)
api = Api(app)

class geeksforgeeksAPI(Resource):
    def get(self, username=""):
        return scrap.fetchResponse(username)


api.add_resource(geeksforgeeksAPI, "/<string:username>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)