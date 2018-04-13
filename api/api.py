from flask import Flask
from flask_cors import CORS
import json
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)

client = MongoClient('mongo', 27017)
db = client.test_database
comparisons = db.comparisons

@app.route('/author/<username1>/<username2>/', methods=['GET'])
def author(username):

    return json.dumps({
        'followers': 0,
        'following': 0,
        'since': 0,
        'avatar': ''
    })

@app.route('/repository/<name1>/<name2>/', methods=['GET'])
def repository(name1, name2):
    compA = {"repo_name":name1,
             "compared_to":name2}
    compB = {"repo_name":name2,
             "compared_to":name1}

    comp = comparisons.insert_one(compA)
    comp = comparisons.insert_one(compB)

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

