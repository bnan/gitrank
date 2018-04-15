from flask import Flask, jsonify
from flask_cors import CORS
from mongoloide import Mongoloide
import github


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = Mongoloide()

@app.route('/api/v1/user/<username1>/<username2>/', methods=['GET'])
def user(username1, username2):
    try:
        users = github.get_users(username1, username2)
        mongo.store_user(users[0]['name'],users[0])
        mongo.store_user(users[1]['name'],users[1])
        averages = mongo.users_average()
        users[0]['score']  = github.calc_user_rank(users[0], averages)
        users[1]['score']  = github.calc_user_rank(users[1], averages)
        return jsonify(**{ 'error': False, 'message': 'success', 'results': {'users': users }})
    except Exception as e:
        return jsonify(**{ 'error': True, 'message': str(e), 'results': {'users': [] }})

@app.route('/api/v1/repository/<name1>/<name2>/', methods=['GET'])
def repository(name1, name2):
    try:
        user1, repo1 = name1.split('.')
        user2, repo2 = name2.split('.')
        repositories = github.get_repositories(user1, repo1, user2, repo2)
        mongo.add_comparison(repositories[0]["name"], repositories[1]["name"])
        mongo.store_repo(repositories[0]["name"], repositories[0])
        mongo.store_repo(repositories[1]["name"], repositories[1])
        averages = mongo.repos_average()
        repositories[0]['score']  = github.calc_repository_rank(repositories[0], averages)
        repositories[1]['score']  = github.calc_repository_rank(repositories[1], averages)
        mongo.store_score(repositories[0]["name"], repositories[0]['score'])
        mongo.store_score(repositories[1]["name"], repositories[1]['score'])
        averages.update(mongo.scores_average())
        averages = {k:float('{0:.2f}'.format(v)) if isinstance(v, (int, float)) else v for k,v in averages.items()}
        history = mongo.get_history(repositories[0]["name"]) + mongo.get_history(repositories[1]["name"])

        results = {
            'repositories': repositories,
            'suggestions': mongo.get_related(name1, name2),
            'averages': averages,
            'history': history
        }
        return jsonify(**{'error': False, 'message': 'success', 'results': results })
    except Exception as e:
        raise e
        return jsonify(**{ 'error': True, 'message': str(e), 'results': {} })


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
