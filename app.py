from flask import Flask
from flask_restful import Resource, Api
from fetch_tweets import fetch_tweets_api
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        tweets = fetch_tweets_api()
        response = jsonify(tweets)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

api.add_resource(HelloWorld, '/fetch_tweets')

if __name__ == '__main__':
    app.run()