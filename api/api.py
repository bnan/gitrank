from flask import Flask, jsonify
from flask_cors import CORS
from mongoloide import Mongoloide


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = Mongoloide()

@app.route('/api/v1/user/<username1>/<username2>/', methods=['GET'])
def user(username1, username2):
    mongo.get_related(username1)
    return jsonify(**{
        'followers': 0,
        'following': 0,
        'since': 0,
        'avatar': ''
    })

@app.route('/api/v1/repository/<name1>/<name2>/', methods=['GET'])
def repository(name1, name2):
    mongo.add_comparison(name1, name2)
    return jsonify(**{
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
