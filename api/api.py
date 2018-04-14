from flask import Flask, jsonify
from flask_cors import CORS
from mongoloide import Mongoloide
import github


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = Mongoloide()

@app.route('/api/v1/user/<username1>/<username2>/', methods=['GET'])
def user(username1, username2):
    users = github.get_users(username1, username2)
    try:
        return jsonify(**{'message': 'success', 'results': users })
    except Exception as e:
        return jsonify(**{ 'message': str(e), 'results': [] })

@app.route('/api/v1/repository/<name1>/<name2>/', methods=['GET'])
def repository(name1, name2):
    mongo.add_comparison(name1, name2)
    mongo.get_related(name1, name2)
    try:
        user1, repo1 = name1.split('.')
        user2, repo2 = name2.split('.')
        repositories = github.get_repositories(user1, repo1, user2, repo2)
        return jsonify(**{'message': 'success', 'results': repositories })
    except Exception as e:
        return jsonify(**{ 'message': str(e), 'results': [] })

@app.route('/test_mean/', methods=['GET'])
def test_mean():
    user= github.get_users("ludeed", "faviouz")
    mongo.store_user("faviouz", user["faviouz"])
    print(mongo.get_user("faviouz"))
    print(mongo.avg())
    return jsonify({"None": "none"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
