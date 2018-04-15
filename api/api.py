from flask import Flask, jsonify
from flask_cors import CORS
from mongoloide import Mongoloide
import github


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = Mongoloide()

@app.route('/api/v1/user/<username1>/<username2>/', methods=['GET'])
def user(username1, username2):
    avg_user = mongo.users_average()

    users = github.get_users(username1, username2)
    try:
        return jsonify(**{ 'error': False, 'message': 'success', 'results': users })
    except Exception as e:
        return jsonify(**{ 'error': True, 'message': str(e), 'results': [] })

@app.route('/api/v1/repository/<name1>/<name2>/', methods=['GET'])
def repository(name1, name2):
    mongo.add_comparison(name1, name2)

    # Related repo based on the given ones
    related = mongo.get_related(name1, name2)

    avg_repo = mongo.repos_average()
    try:
        user1, repo1 = name1.split('.')
        user2, repo2 = name2.split('.')
        repositories = github.get_repositories(user1, repo1, user2, repo2)
        return jsonify(**{'error': False, 'message': 'success', 'results': repositories })
    except Exception as e:
        return jsonify(**{ 'error': True, 'message': str(e), 'results': [] })


@app.route('/test_mean/', methods=['GET'])
def test_mean():
    users = github.get_users("ludeed", "faviouz")
    mongo.store_user(users[0]["name"], users[0])
    mongo.store_user(users[1]["name"], users[1])
    print(mongo.get_user("faviouz"))
    print(mongo.users_average())

    repos = github.get_repositories("facebook", "react", "joaobranquinho", "wake_me_up")
    mongo.store_repo(repos[0]["name"], repos[0])
    mongo.store_repo(repos[1]["name"], repos[1])
    print(mongo.get_repo(repos[0]["name"]))
    print(mongo.get_repo(repos[1]["name"]))
    print(mongo.repos_average())

    return jsonify({"None": "none"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
