from flask import Flask, redirect
from flask_restful import Api, Resource
import scrap

app = Flask(__name__)
api = Api(app)

class geeksforgeeksAPI(Resource):
    def get(self, username=""):
        return scrap.fetchResponse(username)

class redirectToGitRepo(Resource):
    def get(self):
        return redirect("https://github.com/arnoob16/GeeksForGeeksAPI/", code=302)

api.add_resource(geeksforgeeksAPI, "/<string:username>")
api.add_resource(redirectToGitRepo, "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)