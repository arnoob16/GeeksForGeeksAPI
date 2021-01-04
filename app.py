from flask import Flask, current_app
import json
from flask_restful import Api, Resource
from modules.track import track

app = Flask(__name__)
api = Api(app)

class geeksforgeeksAPI(Resource):
    def get(self, username):
        solved = track(username)
        return current_app.response_class(json.dumps(solved.solve(), indent=4), mimetype="application/json")

api.add_resource(geeksforgeeksAPI, "/<string:username>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)