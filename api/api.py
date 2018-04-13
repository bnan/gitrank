from flask import Flask
from flask_cors import CORS
import json
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

#client = MongoClient('mongo', 27017)
#db = client.test_database
#tweets = db.tweets

@app.route('/author/<username>/', methods=['GET'])
def author(username):
    return json.dumps({
        'followers': 0,
        'following': 0,
        'since': 0,
        'avatar': ''
    })

@app.route('/repository/<name>/', methods=['GET'])
def repository(name):
    return json.dumps({
        'stars': 0,
        'forks': 0,
        'branches': 0,
        'commits': 0,
        'latest_commit': 0,
        'contributors': 0,
        'issues': 0,
        'pull_requests': 0,
        'score': 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

