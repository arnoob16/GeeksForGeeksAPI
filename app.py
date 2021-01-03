from flask import Flask, redirect
from flask_restful import Api, Resource
import scrap

app = Flask(__name__)
api = Api(app)

class geeksforgeeksAPI(Resource):
    def get(self, username=""):
        return scrap.fetchResponse(username)


api.add_resource(geeksforgeeksAPI, "/<string:username>")

@app.route("/")
def default_redirect():
    url = "http://github.com/arnoob16/GeeksForGeeksAPI/"
    return redirect(url, code=301)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)