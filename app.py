from flask import Flask, redirect, request
from flask_restful import Api, Resource
import scrap

app = Flask(__name__)
api = Api(app)

class geeksforgeeksAPI(Resource):
    def get(self, username=""):
        if request.path == '/':
            return redirect("https://github.com/arnoob16/GeeksForGeeksAPI/", code=302)
        else:
            return scrap.fetchResponse(username)


api.add_resource(geeksforgeeksAPI, "/", "/<string:username>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)